import datetime
import os
import time

from Database import Database
from Sensors.Sensors import HumiditySensor, PressureSensor, Sensor, TempSensor
from dotenv import load_dotenv


def main() -> None:
    """Entry point."""
    sensors: list[Sensor] = [HumiditySensor(), TempSensor(), PressureSensor()]

    db = Database(os.getenv('DATABASE_PASSWORD'))

    for i in range(5):
        values = [datetime.datetime.now()] + [sensor.value for sensor in sensors]
        db.insert(values)
        time.sleep(1)


if __name__ == '__main__':
    load_dotenv()
    main()
