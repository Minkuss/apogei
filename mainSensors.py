import time

from sensors.sensor import DataPacker
from database.Database import Database


def main() -> None:
    """Entry point."""
    data_packer = DataPacker()
    sensors: list[(str, float)] = data_packer.get_package()

    db = Database()

    values = [data_packer.get_datetime()] + [sensor[1] for sensor in sensors]
    db.insert(values)

    # for row in db.select_all():
    #     print(row)


if __name__ == '__main__':
    main()
