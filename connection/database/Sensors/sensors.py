from random import uniform

from Sensors.BaseSensor import Sensor

# class Sensor(ABC, object):
#     def __init__(self) -> None:
#         self.__value: float = 0
#
#     @abstractmethod
#     def diff(self) -> float:
#         pass
#
#     @property
#     def value(self) -> float:
#         value = self.__value
#         self.__value += self.diff()
#         return value
#
#     @value.setter
#     def value(self, value) -> None:
#         self.__value = value


class TempSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.value = uniform(-25, 25)

    def diff(self):
        """Difference between current value and new value."""
        return uniform(-3, 3)


class PressureSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.value = 100.0

    def diff(self):
        """Difference between current value and new value."""
        return uniform(-5, 5)


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__()
        self.value = 0.7

    def diff(self) -> float:
        """Difference between current value and new value."""
        return uniform(-0.3, 0.3)


if __name__ == '__main__':
    sensor = HumiditySensor()
    for i in range(15):
        print(sensor.value)
