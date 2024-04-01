import datetime
import os
import time

from FakeSensors.sensors import HumiditySensor, PressureSensor, TempSensor
from Database import Database

from dotenv import load_dotenv


def main():
    """Entry point."""
    load_dotenv()
    token = os.environ.get('INFLUXDB_TOKEN')
    org = os.environ.get('ORGANIZATION')
    url = os.environ.get('URL')

    db = Database(token=token, organization=org, url=url)
    db.current_bucket = 'sensors'

    temp = TempSensor()
    pressure = PressureSensor()
    humidity = HumiditySensor()

    # for _ in range(1000):
    #     temp_val = temp.value
    #     pressure_val = pressure.value
    #     humidity_val = humidity.value
    #
    #     measurements = [('Temperature', temp_val),
    #                     ('Pressure', pressure_val),
    #                     ('Humidity', humidity_val)]
    #
    #     db.write(measurements=measurements)
    #
    #     time.sleep(1)

    db.select(end_time=datetime.datetime.now(), minutes_delta=30)


if __name__ == '__main__':
    main()
