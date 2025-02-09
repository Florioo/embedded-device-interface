from pydantic import BaseModel
import struct
import colorsys
from abc import ABC, abstractmethod
from enum import Enum

AUTH_INFO = 0x00010000
RGB_LED = 0x0A000000
SERVO_FRONT_LEFT = 0x01010000
SERVO_FRONT_RIGHT = 0x01020000
SERVO_BACK_LEFT = 0x01030000
SERVO_BACK_RIGHT = 0x01040000
SERVO_BACK_CENTER_LEFT = 0x01050000
SERVO_BACK_CENTER_RIGHT = 0x01060000


class GenericModel(BaseModel, ABC):
    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes):
        pass

    ID: int


class RGBLed(GenericModel):
    ID: int = RGB_LED
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
        return RGBLed(
            red=int(r * 255), green=int(g * 255), blue=int(b * 255)
        )

class RGBColors(Enum):
    RED = RGBLed(red=255, green=0, blue=0)
    GREEN = RGBLed(red=0, green=255, blue=0)
    BLUE = RGBLed(red=0, green=0, blue=255)
    INVALID_BLUE = RGBLed(red=0, green=0, blue=255, ID=0x0A000001)
    
class Servo(GenericModel):
    value: int

    def encode(self) -> bytes:
        return struct.pack("f", self.value)

    def decode(self, data: bytes):
        self.value = struct.unpack("f", data)[0]
