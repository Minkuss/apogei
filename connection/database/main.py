import os
import time

from Sensors.sensors import HumiditySensor, PressureSensor, TempSensor

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    """Entry point."""
    token = os.environ.get('INFLUXDB_TOKEN')
    org = 'apogei'
    url = 'http://localhost:8086'

    temp = TempSensor()
    pressure = PressureSensor()
    humidity = HumiditySensor()

    client = InfluxDBClient(url=url, org=org, token=token)

    bucket = 'sensors'

    write_api = client.write_api(write_options=SYNCHRONOUS)

    for _ in range(1000):
        temp_val = temp.value
        pressure_val = pressure.value
        humidity_val = humidity.value

        point = (
            Point('environment')
            .field('Temperature', temp_val)
            .field('Pressure', pressure_val)
            .field('Humidity', humidity_val)
        )

        print(f'Writing {point.to_line_protocol()}')
        write_api.write(bucket=bucket, org=org, record=point)
        time.sleep(1)


if __name__ == '__main__':
    main()
