import time
import schedule
import threading
import datetime

from sensors.sensor import DataPacker
from database.Database import Database
from connection.server.server import main as main_connection


def insert_values() -> None:
    """Insert new data pack to database every specified time."""
    data_packer = DataPacker()
    values: [datetime.datetime, float] = data_packer.get_bd_package()

    db = Database()
    db.insert(values)

    print('An hour left; New pack of data inserted.')


def run_schedule() -> None:
    """Run schedule functions."""
    schedule.every().hour.do(insert_values)
    schedule.every().day.do(Database.clear_old_data)

    while True:
        schedule.run_pending()
        time.sleep(1)


def thread_schedule() -> None:
    """Create thread for control schedule."""
    db_thread = threading.Thread(target=run_schedule)
    db_thread.start()


if __name__ == '__main__':
    """Entry point."""
    thread_schedule()
    main_connection(Database())
