from sensor_measurement_parser import BluetoothParser


def main():
    parser = BluetoothParser()
    responses = []
    for c in "LOCALIZE,1\n":
        r = parser.add_data(c)
        responses.append(r)
    for c in "1,2,3,4\n":
        r = parser.add_data(c)
        responses.append(r)
    assert responses == [None] * 11 + [None] * 7 + [("LOCALIZE", 1, 1, 2, 3, 4)]


if __name__ == "__main__":
    main()