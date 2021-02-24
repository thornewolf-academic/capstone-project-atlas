import copy
import itertools
from collections import defaultdict

import numpy as np
import pandas as pd
import uncertainties
import time
from uncertainties import umath
from uncertainties import unumpy as unp

from utilities import SYSTEM_STATES, Subscribable, Subscriber, UpdateSignal

STEPS_PER_ROTATION = 3200
LIDAR_UNCERT = 0.025


class PointCloudGenerator(Subscribable, Subscriber):
    def __init__(self, point_cloud_file_name):
        super().__init__()

        self.point_cloud_file_name = point_cloud_file_name
        self.target_measurements = defaultdict(lambda: defaultdict(tuple))
        self.scan_measurements = defaultdict(list)
        self.my_locations = defaultdict(tuple)
        self.target_locations = defaultdict(lambda: defaultdict(tuple))
        self.scan_locations = defaultdict(list)
        self.iteration = None
        self.last_save = time.time()

    def signal(self, signal: UpdateSignal, data=None):
        if signal == UpdateSignal.NEW_DATA:
            self.handle_new_data(data)
        return super().signal(signal, data=data)

    def handle_new_data(self, data):
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
            measurement = tuple(data[2:])
            self.scan_measurements[state_iteration].append(measurement)
            self.scan_locations[state_iteration].append(
                self.measurement_to_location(measurement)
            )
            if time.time() - self.last_save > 1:
                self.save_scan()
                self.last_save = time.time()

            self.signal_subscribers(UpdateSignal.NEW_DATA)

    def measurement_to_location(self, measurement):
        R = self.generate_rotation_matrix()
        relative_location = np.matmul(R, measurement_to_xyz(measurement))
        inertial_location = self.my_locations[self.iteration] + relative_location
        return inertial_location

    def generate_rotation_matrix(self):
        # TODO: handle multiple targets
        targets = self.target_measurements[self.iteration]
        t1 = targets[1]
        t2 = targets[2]
        p1 = measurement_to_xyz(t1)
        p2 = measurement_to_xyz(t2)
        xax = np.reshape(unp.uarray([1, 0, 0], [0.0, 0.0, 0.0]), (3,))
        p2p1 = p2 - p1
        R = rotation_matrix_from(p2p1, xax)
        self.my_locations[self.iteration] = np.matmul(R, -p1.copy())
        return R

    def save_scan(self):
        locs = []
        for iteration in self.scan_locations.keys():
            locs += self.scan_locations[iteration]
        print(len(locs))
        locs = np.array(locs)
        locs = np.squeeze(locs, axis=(1,))
        locs = unp.nominal_values(locs)
        np.save(self.point_cloud_file_name, locs)


def unorm(v):
    return (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5


def rotation_matrix_from(A, B):
    A = A / unorm(A)
    B = B / unorm(B)

    v = np.cross(A, B)
    s = unorm(v)
    c = np.dot(A, B)

    ssm = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    R = np.eye(3) + ssm + np.matmul(ssm, ssm) / (1 + c)
    R = unp.matrix(R)
    return R


def measurement_to_xyz(measurement):
    theta_step, phi_step, dist = measurement
    dist = uncertainties.ufloat(dist, LIDAR_UNCERT)
    theta_step = uncertainties.ufloat(theta_step, 0.05)
    phi_step = uncertainties.ufloat(phi_step, 0.05)
    return np.array(
        [
            dist
            * umath.cos(theta_step * 360 / STEPS_PER_ROTATION * np.pi / 180)
            * umath.cos(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
            dist
            * umath.sin(theta_step * 360 / STEPS_PER_ROTATION * np.pi / 180)
            * umath.cos(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
            dist * umath.sin(phi_step * 360 / STEPS_PER_ROTATION * np.pi / 180),
        ]
    )


if __name__ == "__main__":
    gen = PointCloudGenerator("temp")
    t1 = ("LOCALIZE", 1, 1, 0, 0, 0)
    t2 = ("LOCALIZE", 1, 2, 10, 0, 0)

    (gen.signal(UpdateSignal.NEW_DATA, t1))
    (gen.signal(UpdateSignal.NEW_DATA, t2))
    p1 = ("SCAN", 1, 5, 0, 50)
    (gen.signal(UpdateSignal.NEW_DATA, p1))
    (gen.signal(UpdateSignal.NEW_DATA, p1))

    (gen.target_measurements)
    (gen.scan_measurements)
    (gen.my_locations[1])
    locs = gen.scan_locations[1]
    locs = np.array(locs)
    locs = np.squeeze(locs, axis=(1,))
    locs = unp.nominal_values(locs)