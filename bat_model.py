class BatteryModel:
    # Duration in seconds please
    def __init__(self, peak, end, duration, current, isr = 0):
        self.v = peak
        self.gradient = (peak - end) / duration
        self.current = current
        self.isr = isr
        self.boundary = (peak, end)

    def use(self, duration):
        self.v = self.v - duration * self.gradient
        if self.v < self.boundary[1]:
            raise Exception("Battery model exceeds boundaries")
