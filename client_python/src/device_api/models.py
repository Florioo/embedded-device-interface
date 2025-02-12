import colorsys
import struct
from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel


class GenericModel(BaseModel, ABC):
    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes):
        pass
    
    ID: int= 0


class RGBLed(GenericModel):
    red: int
    green: int
    blue: int

    def encode(self) -> bytes:
        return struct.pack("BBB", self.red, self.green, self.blue)

    def decode(self, data: bytes):
        self.red, self.green, self.blue = struct.unpack("BBB", data)

    @classmethod
    def from_hsv(cls, hue: float, saturation: float, value: float):
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return RGBLed(red=int(r * 255), green=int(g * 255), blue=int(b * 255))


class RGBColors(Enum):
    RED = RGBLed(red=255, green=0, blue=0)
    GREEN = RGBLed(red=0, green=255, blue=0)
    BLUE = RGBLed(red=0, green=0, blue=255)
    WHITE = RGBLed(red=255, green=255, blue=255)


class Servo(GenericModel):
    value: int

    def encode(self) -> bytes:
        return struct.pack("f", self.value)

    def decode(self, data: bytes):
        self.value = struct.unpack("f", data)[0]
