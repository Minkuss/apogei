import time
import schedule
import threading

from sensors.sensor import DataPacker
from database.Database import Database
from connection.server.server import main as main_connection


def insert_values() -> None:
    """Insert new data pack to database every specified time."""
    data_packer = DataPacker()
    sensors: list[(str, float)] = data_packer.get_package()

    db = Database()

    values = [data_packer.get_datetime()] + [sensor[1] for sensor in sensors]
    db.insert(values)

    print('20 seconds left; New pack of data inserted.')


def run_schedule() -> None:
    """Run schedule functions."""
    schedule.every(20).seconds.do(insert_values)
    schedule.every().day.do(Database.clear_old_data)

    while True:
        schedule.run_pending()
        time.sleep(1)


def main_db() -> None:
    """Create thread for control schedule."""
    db_thread = threading.Thread(target=run_schedule)
    db_thread.start()


if __name__ == '__main__':
    """Entry point."""
    main_db()
    main_connection(Database())
