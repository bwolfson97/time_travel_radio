# AUTOGENERATED! DO NOT EDIT! File to edit: 01_controls.ipynb (unless otherwise specified).

__all__ = ['ADCDevice', 'ADS7830', 'DecadesDial', 'PowerButton']

# Cell
import time
import smbus
from .core import *
import numpy as np
from gpiozero import Button
import os
from typing import *

# Cell
class ADCDevice:
    """ADC device that automatically closes itself when destroyed."""
    def __init__(self):
        self.cmd = 0
        self.address = 0
        self.bus=smbus.SMBus(1)

    def close(self):    self.bus.close()
    def __del__(self):  self.close()
    def __exit__(self): self.close()

# Cell
class ADS7830(ADCDevice):
    def __init__(self):
        super().__init__()
        self.cmd = 0x84
        self.address = 0x4b # 0x4b is the default i2c address for ADS7830 Module.

    def analogRead(self, chn): # ADS7830 has 8 ADC input pins, chn:0,1,2,3,4,5,6,7
        value = self.bus.read_byte_data(self.address, self.cmd|(((chn<<2 | chn>>1)&0x07)<<4))
        return value

    @staticmethod
    def value_range():
        """Returns range of values device can represent."""
        return 2**8 - 1  # This is an 8-bit ADC

# Cell
class DecadesDial(ADS7830):
    """Potentiometer linked to ADS7830 ADC converts read value into decade."""
    def __init__(self, decades: Dict[str, str]):
        super().__init__()
        self.decades = [decade for decade in decades]
        self.bins = self._build_bins(len(decades))

    def read_decade(self):
        """Reads value from potentiometer and returns the corresponding decade."""
        value = self.analogRead(0)  # B/c potentiometer is connected to channel 0 of ADC
        bin_idx = np.digitize(value, self.bins)
        return self.decades[bin_idx]

    def _build_bins(self, num_bins: int):
        """Builds bin of potentiometer values corresponding to each decade."""
        bin_size = self.value_range() / num_bins
        bins = [bin_size * i for i in range(1, num_bins)]
        return bins

# Cell
class PowerButton(Button):
    """Creates a power button for the Raspberry Pi.

    Shuts down the Pi after being held down for 5
    seconds.
    """
    def __init__(self, gpio_pin: int):
        """Creates power button from button connected to gpio_pin."""
        super().__init__(gpio_pin, hold_time=5)  # must hold for 5 seconds

    @staticmethod
    def when_held():
        """Shuts down Raspberry Pi."""
        os.system("sudo shutdown -h now")