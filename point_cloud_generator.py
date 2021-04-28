from collections import defaultdict
from re import A

import numpy as np
from numpy.core.fromnumeric import shape
import pandas as pd
import uncertainties
import time
from uncertainties import umath
from uncertainties import unumpy as unp

import itertools as it
from utilities import SYSTEM_STATES, Subscribable, Subscriber, UpdateSignal
import logging
from typing import Union, List

import sys

STEPS_PER_ROTATION = 3200
LIDAR_UNCERT = 0.05


class PointCloudGenerator(Subscribable, Subscriber):
    def __init__(self, config):
        super().__init__()

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        self.logger = logging.getLogger("point_cloud_generator")
        self.logger.addHandler(ch)

        self.real_time_point_cloud_file_name = config["real_time_point_cloud_name"]
        self.final_point_cloud_file_name = config["final_point_cloud_name"]
        self.target_locations_file_name = config["sensor_package_locations_name"]
        self.target_measurements = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: None))
        )
        self.my_locations = defaultdict(tuple)
        self.total_locations = 0
        self.scan_locations_list = []
        self.scan_locations = np.zeros((1, 4))
        self.iteration = None
        self.last_save = time.time()
        self.finished = False

        self._target_locations = defaultdict(lambda: defaultdict(lambda: None))
        self._rotation_matrices = defaultdict(lambda: None)
        self._origin_target = None
        self.targets_set = set()

    def signal(self, signal: UpdateSignal, data=None):
        # self.logger.info(f"Signaled with new data.")
        if signal == UpdateSignal.NEW_DATA:
            self.handle_new_data(data)
        return super().signal(signal, data=data)

    def mark_finished(self):
        self.logger.info(f"Marking self as finished.")
        self.save_scan()
        self.save_scan(final_scan=True)
        self.finished = True

    def handle_new_data(self, data: List[str]):
        # self.logger.info(f"New data received\n\t{data=}")

        system_state = data[0]

        if system_state == SYSTEM_STATES.LOCALIZE:
            state_iteration = data[1]
            self.iteration = state_iteration
            target_id = data[2]
            self.target_measurements[state_iteration][target_id] = tuple(data[3:])
            return
        if system_state == SYSTEM_STATES.SCAN:
            state_iteration = data[1]
            self.iteration = state_iteration

            # Insert measurement into raw measurements data structure
            measurement = tuple(data[2:])

            # Convert measurement to inertial location and store
            location = self.measurement_to_location(measurement)
            location = np.append([state_iteration], location, axis=0)

            # self.logger.info(f"{self.scan_locations=}")
            self.scan_locations_list.append(location)

            # Hardcoded rate-limit on save frequency for performance
            if time.time() - self.last_save > 2:
                self.save_scan()
                self.last_save = time.time()

            self.signal_subscribers(UpdateSignal.NEW_DATA)

    def measurement_to_location(self, measurement):
        R = self.get_or_generate_rotation_matrix()
        relative_location = np.matmul(R, measurement_to_xyz(measurement))
        inertial_location = self.my_locations[self.iteration] + relative_location
        return inertial_location

    def get_or_generate_rotation_matrix(self):
        if self._rotation_matrices[self.iteration] is not None:
            return self._rotation_matrices[self.iteration]

        self.get_or_generate_target_locations()
        return self._rotation_matrices[self.iteration]

    @property
    def target_locations(self):
        return self.get_or_generate_target_locations()

    def get_or_generate_target_locations(self):
        if len(self._target_locations[self.iteration]) > 0:
            return self._target_locations

        target_measurements = self.target_measurements[self.iteration]

        # # Align all targets as according to origin target.
        # if self._origin_target is None:
        #     self._origin_target = min(target_measurements)

        relative_locations = {
            tid: measurement_to_xyz(measurment)
            for tid, measurment in target_measurements.items()
        }

        # Keep track of all targets we have ever seen
        for tid in target_measurements.keys():
            self.targets_set.add(tid)

        # Determine what two targets we have enough information on to make calculations on.
        # We need to know what their locations were last iteration and what they are this iteration.
        target_1 = None
        target_2 = None
        for ct1, ct2 in it.combinations(self.targets_set, r=2):
            if (
                ct1 in self._target_locations[self.iteration - 1]
                and ct2 in self._target_locations[self.iteration - 1]
                and ct1 in relative_locations
                and ct2 in relative_locations
            ):
                target_1 = ct1
                target_2 = ct2
                break

        if target_1 is None:
            target_1, target_2 = sorted(target_measurements)[:2]
            self._origin_target = target_1

        measured_axis = relative_locations[target_2] - relative_locations[target_1]

        if (
            target_1 in self._target_locations[self.iteration - 1]
            and target_2 in self._target_locations[self.iteration - 1]
        ):
            true_axis = (
                self._target_locations[1][target_2]
                - self._target_locations[1][target_1]
            )
        else:
            true_axis = np.reshape([1, 0, 0], (3,))

        true_axis = np.reshape(true_axis, (3,))

        R = rotation_matrix_from(measured_axis, true_axis)
        self._rotation_matrices[self.iteration] = R

        sensor_relative_location_to_origin = -np.matmul(
            R, relative_locations[target_1].copy()
        )

        inertial_locations = {
            tid: np.asarray(np.matmul(R, measurement.copy()))
            for tid, measurement in relative_locations.items()
        }

        inertial_offset = None
        for tid in sorted(inertial_locations):
            if tid in sorted(self._target_locations[1]):
                inertial_offset = (
                    inertial_locations[tid] - self._target_locations[1][tid]
                )
                break
        if inertial_offset is None:
            inertial_offset = inertial_locations[target_1]

        self.logger.info(
            f"Need inertial offset of {inertial_offset} to correct {tid} from\n{inertial_locations[tid]} -> {inertial_locations[tid]-inertial_offset}"
        )

        self.my_locations[self.iteration] = sensor_relative_location_to_origin
        self.logger.info(
            f"I believe the sensor package is at {self.my_locations[self.iteration]=}"
        )

        for tid, location in inertial_locations.items():
            self._target_locations[self.iteration][tid] = location - inertial_offset

        try:
            self.logger.info(f"{self._target_locations[self.iteration][1]=}")
            self.logger.info(f"{self._target_locations[self.iteration][2]=}")
            self.logger.info(f"{self._target_locations[self.iteration][3]=}")
        except:
            pass

        return self._target_locations

    def save_scan(self, final_scan=False):
        # TODO(thorne): The shape of the saved scan is likely (n,8) instead of (n,7) this is because there is an uncertainty measurement related with the iteration number. Fix this.
        # Save all scanned points
        new_scan_locations = np.reshape(np.array(self.scan_locations_list), (-1, 4))
        self.scan_locations = np.append(self.scan_locations, new_scan_locations, axis=0)
        self.scan_locations_list = []

        target_locs = []
        for iteration in self.target_locations.keys():
            for target_id in self.target_locations[iteration].keys():
                data = np.append(
                    [iteration, target_id],
                    unp.nominal_values(
                        self.target_locations[iteration][target_id]
                    ).tolist(),
                )
                target_locs += [data]
        target_locs = np.array(target_locs)

        self.logger.info(f"Total locations {len(self.scan_locations)}")
        if not final_scan:
            np.save(self.real_time_point_cloud_file_name, self.scan_locations)
            np.save(self.target_locations_file_name, target_locs)
            return

        raw = unp.nominal_values(self.scan_locations)
        stds = unp.std_devs(self.scan_locations)
        total_data = np.concatenate((raw, stds), axis=1)
        np.save(self.real_time_point_cloud_file_name, self.scan_locations)
        np.save(self.final_point_cloud_file_name, total_data)
        np.save(self.target_locations_file_name, target_locs)


def unorm(v):
    v = np.reshape(v, (3, 1))
    mag = np.power(v[0] ** 2 + v[1] ** 2 + v[2] ** 2, 0.5)
    return mag


def rotation_matrix_from(A, B):
    A = A / unorm(A)
    B = B / unorm(B)

    v = np.cross(A, B)
    s = unorm(v)
    c = np.dot(A, B)

    ssm = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    R = np.eye(3) + ssm + np.matmul(ssm, ssm) / (1 + c)
    return R


def measurement_to_xyz(measurement):
    try:
        theta_step, phi_step, dist = measurement
    except Exception as e:
        print("unpacking point failed")
        return np.array([0, 0, 0])
    # dist = uncertainties.ufloat(dist, LIDAR_UNCERT)
    # theta_step = uncertainties.ufloat(theta_step, 0.05)
    # phi_step = uncertainties.ufloat(-phi_step, 0.05)
    theta_step = theta_step
    phi_step = -phi_step
    return np.array(
        [
            dist
            * np.math.cos(theta_step * 360 / STEPS_PER_ROTATION * np.pi / 180)
            * np.math.cos(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
            dist
            * np.math.sin(theta_step * 360 / STEPS_PER_ROTATION * np.pi / 180)
            * np.math.cos(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
            dist * np.math.sin(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
        ]
    )