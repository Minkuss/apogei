import board
import busio
import adafruit_ds3231
import Adafruit_BMP.BMP085
import Adafruit_DHT
import datetime
import smbus
# import time


class DateTimeSensor:
    def __init__(self) -> None:
        self.ds3231 = adafruit_ds3231.DS3231(busio.I2C(board.SCL, board.SDA))
        self.__set_time()

    def __set_time(self) -> None:
        self.ds3231.datetime = datetime.datetime.now().timetuple()

    def get_sensor_status(self) -> datetime.datetime:
        return self.ds3231.datetime


class PressureSensor:
    def __init__(self) -> None:
        self.bmp = Adafruit_BMP.BMP085.BMP085()

    def get_pressure_sensor_status(self) -> float:
        return float(self.bmp.read_pressure())

    def get_temperature_sensor_status(self) -> float:
        return float(self.bmp.read_temperature())


class HumiditySensor:
    def __init__(self) -> None:
        self.dht_sensor = Adafruit_DHT.DHT22
        self.dht_pin = 14

    def get_humidity_sensor_status(self) -> float:
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
        return float(humidity)

    def get_temperature_sensor_status(self) -> float:
        humidity, temperature = Adafruit_DHT.read_retry(self.dht_sensor, self.dht_pin)
        return float(temperature)


class IlluminationSensor:
    def __init__(self) -> None:
        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # TSL2561 address, 0x39(57)
        # Select control register, 0x00(00) with command register, 0x80(128)
        self.bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        self.bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

    def __read_data(self) -> [bytes, bytes]:
        # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
        data = self.bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

        # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = self.bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
        return [data, data1]

    def get_full_spectrum(self) -> float:
        data, data1 = self.__read_data()

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        return float(ch0)

    def get_infrared_spectrum(self) -> float:
        data, data1 = self.__read_data()

        # Convert the data
        ch1 = data1[1] * 256 + data1[0]
        return float(ch1)

    def get_visible_spectrum(self) -> float:
        data, data1 = self.__read_data()

        # Convert the data
        ch0 = data[1] * 256 + data[0]
        ch1 = data1[1] * 256 + data1[0]
        return float(ch0 - ch1)


class DataPacker:
    def __init__(self) -> None:
        self.time_sensor = DateTimeSensor()
        self.pressure_sensor = PressureSensor()
        self.humidity_sensor = HumiditySensor()
        self.lux_sensor = IlluminationSensor()

    def get_datetime(self) -> datetime.datetime:
        return self.time_sensor.get_sensor_status()

    def get_package(self) -> [("", float)]:
        return [("Pressure", self.pressure_sensor.get_pressure_sensor_status()),
                ("Humidity", self.humidity_sensor.get_humidity_sensor_status()),
                ("Temperature(pressure)", self.pressure_sensor.get_temperature_sensor_status()),
                ("Temperature(humidity)", self.humidity_sensor.get_temperature_sensor_status()),
                ("Full spectrum", self.lux_sensor.get_full_spectrum()),
                ("Infrared spectrum", self.lux_sensor.get_infrared_spectrum()),
                ("Visible spectrum", self.lux_sensor.get_visible_spectrum())]


if __name__ == '__main__':
    # Uncomment to check the performance
    # packer = DataPacker()
    #
    # while True:
    #     datetime = packer.get_datetime()
    #     package = packer.get_package()
    #     print("Время: {}:{}:{}".format(datetime.tm_hour, datetime.tm_min, datetime.tm_sec))
    #     print("Дата: {}-{}-{}".format(datetime.tm_year, datetime.tm_mon, datetime.tm_mday))
    #     for data in package:
    #         print(*data)
    #     print()
    #     time.sleep(4)
    pass
