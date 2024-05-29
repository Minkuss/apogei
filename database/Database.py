import datetime
import numpy as np

from database.Sensors.Sensors import HumiditySensor, TempSensor, PressureSensor

import sqlalchemy
from sqlalchemy import Column, Insert, MetaData, Table, create_engine, exc, insert, select, delete
from sqlalchemy_utils import create_database, database_exists


class Database(object):
    def __init__(self, dbname: str = 'mydb', echo: bool = False):
        if not dbname.endswith('.db'):
            dbname += '.db'

        self.__engine = create_engine(f'sqlite:///{dbname}', echo=echo)

        self.__metadata = MetaData()
        COLUMN_NAMES = ['pressure', 'humidity', 'temperature', 'full_spectrum', 'infrared_spectrum', 'visible_spectrum']
        COLUMNS = [Column(column_name, sqlalchemy.DECIMAL(4, 2, asdecimal=False))
                   for column_name in COLUMN_NAMES]
        Table('sensors', self.__metadata,
              Column('timestamp', sqlalchemy.TIMESTAMP, primary_key=True),
              *COLUMNS)

        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)

        self.__metadata.create_all(self.__engine)
        self.__sensors = self.__metadata.tables['sensors']

    def insert(self, values: list[datetime.datetime | float]) -> None:
        """
        Insert sensor values into table.

        :param values: list where first value is datetime and other 6 is float
        :return: None
        """
        insert_query: Insert = insert(self.__sensors).values(values)
        with self.__engine.connect() as conn:
            try:
                conn.execute(insert_query)
                conn.commit()
            except exc.SQLAlchemyError as e:
                print(e.args)
                conn.rollback()

    def insert_distributed_data(self, data: list[list[float]], with_noise: bool = False, samples: int = 4):
        """
        Evenly distribute data with half of hour intervals.

        :param data: lisf of rows to distribute
        :param with_noise: if True make new data with normal noise
        :param samples: shows how many times the data set will increase
        :return: None
        """
        insert_data = data.copy()
        now = datetime.datetime.now()

        if with_noise:
            noise_data = []
            for row in data:
                noise_data += self.add_noise(row, samples)
            insert_data = noise_data

        start_time = now - datetime.timedelta(minutes=30 * (len(insert_data) // 2))
        for row in insert_data:
            self.insert([start_time] + row)
            start_time += datetime.timedelta(minutes=30)

    @staticmethod
    def add_noise(data: list[float], samples: int) -> list[list[float]]:
        """
        Make new rows with normal noise.

        :param data: initial row
        :param samples: how many samples will be created
        :return: data with normal noise
        """
        data = np.array(data)
        noise_data = []
        for i in range(samples):
            noise_row = data + np.random.normal(0, 2, len(data))
            noise_data.append(noise_row.round(2).tolist())
        return noise_data

    def insert_fake_data(self, count: int):
        """
        Insert sensor values into table.

        :param count: list where first value is datetime and other 6 is float
        :return: None
        """
        assert count > 0, 'Number of rows must be positive'

        sensors: list = [HumiditySensor(), TempSensor(), PressureSensor()]

        for i in range(count):
            values: list[datetime.datetime | float] = ([datetime.datetime.now() + datetime.timedelta(minutes=i)] +
                                                       [round(sensor.value, 2) for sensor in sensors])
            self.insert(values)

    def select_by_timestamp_range(self, end_time: datetime.datetime, minutes_diff: int):
        """Select data in time range from database as alchemy classes."""
        start_time = end_time - datetime.timedelta(minutes=minutes_diff)
        query = select(self.__sensors).where(self.__sensors.c['timestamp'] <= end_time,
                                             self.__sensors.c['timestamp'] >= start_time)
        print(query)
        with self.__engine.connect() as conn:
            try:
                result = conn.execute(query)
                return result
            except exc.SQLAlchemyError as e:
                print(e.args)

    def select_all(self):
        """Select all data from database as alchemy classes."""
        with self.__engine.connect() as conn:
            result = conn.execute(select(self.__sensors)).all()
        return result

    def select_all_as_dict(self):
        """Select all data from database as json objects."""
        with self.__engine.connect() as conn:
            result = conn.execute(select(self.__sensors)).all()

        data = []
        for row in result:
            dict_row = row._asdict()
            for key, value in dict_row.items():
                # if value is None:
                #     continue
                if isinstance(value, datetime.datetime):
                    dict_row[key] = value.isoformat()

            data.append(dict_row)

        return data

    def clear_old_data(self, age_days: int = 1):
        """Delete old data from database.

        :param age_days: determine how old data will be removed from database
        """
        assert age_days >= 0, 'Count of days must be non negative'

        threshold = datetime.datetime.now() - datetime.timedelta(days=age_days)
        query = delete(self.__sensors).where(self.__sensors.c['timestamp'] <= threshold)
        with self.__engine.connect() as conn:
            conn.execute(query)
            conn.commit()

    def clear(self):
        """Delete all data from database."""
        with self.__engine.connect() as conn:
            conn.execute(delete(self.__sensors))
            conn.commit()


def main() -> None:
    """Entry point."""
    db: Database = Database(echo=False)
    db.clear()
    data = np.random.uniform(low=-15, high=15, size=(4, 6)).round(2).tolist()
    db.insert_distributed_data(data, with_noise=True, samples=10)
    data = db.select_all_as_dict()
    print(*data, len(data), sep='\n')


if __name__ == '__main__':
    main()
