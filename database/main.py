import datetime
import time

from Database import Database
from Sensors.Sensors import HumiditySensor, PressureSensor, Sensor, TempSensor


def main() -> None:
    """Entry point."""
    sensors: list[Sensor] = [HumiditySensor(), TempSensor(), PressureSensor()]

    db = Database()

    for i in range(5):
        values = [datetime.datetime.now()] + [sensor.value for sensor in sensors]
        db.insert(values)
        time.sleep(1)

    result = db.select_by_timestamp_range(datetime.datetime.now(), 20)
    for row in result:
        print(row)


if __name__ == '__main__':
    main()
