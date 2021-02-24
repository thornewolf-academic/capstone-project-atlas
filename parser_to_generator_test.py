from utilities import UpdateSignal
from sensor_measurement_parser import BluetoothParser
from point_cloud_generator import PointCloudGenerator

def main():
    parser = BluetoothParser()
    gen = PointCloudGenerator('mypointcloud')
    with open('multi_location_data','r') as f:
        data = f.read()
    for i,c in enumerate(data[:]):
        r = parser.add_data(c)
        if r is not None:
            gen.signal(UpdateSignal.NEW_DATA, r)
            if r[0] == 'SCAN':
                pass
    print(gen.scan_measurements[1])

if __name__ == '__main__':
    main()