import datetime

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

    def insert_fake_data(self, count: int):
        """
        Insert sensor values into table.

        :param count: list where first value is datetime and other 6 is float
        :return: None
        """

        assert count > 0, "Number of rows must be positive"

        sensors: list = [HumiditySensor(), TempSensor(), PressureSensor()]

        for _ in range(count):
            values: list[datetime.datetime | float] = [datetime.datetime.now()] + [round(sensor.value, 2)
                                                                                   for sensor in sensors]
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

        assert age_days >= 0, "Count of days must be non negative"

        threshold = datetime.datetime.now() - datetime.timedelta(days=age_days)
        query = delete(self.__sensors).where(self.__sensors.c['timestamp'] <= threshold)
        with self.__engine.connect() as conn:
            conn.execute(query)
            conn.commit()


def main() -> None:
    """Entry point."""
    db: Database = Database(echo=True)
    sensors: list = [HumiditySensor(), TempSensor(), PressureSensor()]
    values: list[datetime.datetime | float] = [datetime.datetime.now()] + [round(sensor.value, 2) for sensor in sensors]
    db.insert(values)
    data = db.select_all_as_dict()
    print(data)
    # db.clear_old_data(age_days=1)


if __name__ == '__main__':
    main()
