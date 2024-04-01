from datetime import datetime, timedelta
import time

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class Database():
    def __init__(self, organization: str, url: str, token: str):
        self.__org = organization
        # self.__url = url
        self.__token = token
        self.current_bucket = ""

        self.__client = InfluxDBClient(org=organization, url=url, token=token)

    def write(self, measurements: list[tuple[str, float]], timestamp: datetime = None):
        if self.current_bucket == "":
            raise ValueError("bucket  isn't specified")

        write_api = self.__client.write_api(write_options=SYNCHRONOUS)
        point = Point("environment")

        if timestamp is not None:
            point.time(timestamp)

        for measurement_name, measurement in measurements:
            point.field(measurement_name, measurement)

        write_api.write(bucket=self.current_bucket, record=point, write_precision="ms")

        print(point.to_line_protocol(), "is written")

    def select(self, end_time: datetime, minutes_delta: float):
        start_time = end_time - timedelta(minutes=minutes_delta)

        start_time_format = int(time.mktime(start_time.timetuple()))
        api = self.__client.query_api()
        query = f"""from(bucket: "{self.current_bucket}")
                    |> range(start: {start_time_format})
                    |> filter(fn: (r) => r._measurement == "environment")"""
        tables = api.query(query, org=self.__org)

        for table in tables:
            for record in table.records:
                print(record)
