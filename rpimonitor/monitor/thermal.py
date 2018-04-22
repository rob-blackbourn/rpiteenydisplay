"""Thermal monitoring"""

class Temp(object):
    """Class for reading /sys/class/thermal/thermal_zone0/temp"""

    def __init__(self, temp):
        self.temp = temp

    @classmethod
    def _parse(cls, line):
        """Parse the temperature"""
        return Temp(float(line) / 1000)

    @classmethod
    def sample(cls):
        """Sample CPU temperature"""
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return cls._parse(f.readline())

    def __str__(self):
        return f"temp: {self.temp}"
    
if __name__ == "__main__":
    temp = Temp.sample()
    print(str(temp))
