import datetime

import sqlalchemy
from sqlalchemy import Column, Insert, MetaData, Table, create_engine, exc, insert, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists


class Database(object):
    def __init__(self,  dbname: str = 'mydb'):
        if not dbname.endswith(".db"):
            dbname += ".db"

        self.__engine = create_engine(f'sqlite:///{dbname}', echo=False)

        self.__metadata = MetaData()
        Table('sensors', self.__metadata,
              Column('timestamp', sqlalchemy.TIMESTAMP, primary_key=True),
              Column('pressure', sqlalchemy.DECIMAL(6, 1)),
              Column('humidity', sqlalchemy.DECIMAL(6, 1)),
              Column('temperature', sqlalchemy.DECIMAL(6, 1)),
              Column('full_spectrum', sqlalchemy.DECIMAL(6, 1)),
              Column('infrared_spectrum', sqlalchemy.DECIMAL(6, 1)),
              Column('visible_spectrum', sqlalchemy.DECIMAL(6, 1))),

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

    def select_by_timestamp_range(self, end_time: datetime.datetime, minutes_diff: int):
        start_time = end_time - datetime.timedelta(minutes=minutes_diff)
        query = select(self.__sensors).where(self.__sensors.c["timestamp"] <= end_time,
                                             self.__sensors.c["timestamp"] >= start_time)
        print(query)
        with self.__engine.connect() as conn:
            try:
                result = conn.execute(query)
                return result
            except exc.SQLAlchemyError as e:
                print(e.args)

    def select_all(self):
        session = sessionmaker(bind=self.__engine)()
        query = session.query(self.__sensors).all()
        session.close()
        return query


def main() -> None:
    """Entry point."""
    db: Database = Database()
    values: list[datetime.datetime | float] = [datetime.datetime.now()]
    print(values)
    db.insert(values)


if __name__ == '__main__':
    main()
