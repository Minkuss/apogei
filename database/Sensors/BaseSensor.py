from abc import ABC, abstractmethod


class Sensor(ABC, object):
    """Representation of a sensor with a fictive data."""

    def __init__(self) -> None:
        """Initialize variables."""
        self.__value: float = 0

    @abstractmethod
    def diff(self) -> float:
        """Difference between current value and new value."""
        pass

    @property
    def value(self) -> float:
        """Getter for the value of the sensor."""
        value = self.__value
        self.__value += self.diff()
        return value

    @value.setter
    def value(self, value) -> None:
        """Setter for the value of the sensor."""
        self.__value = value