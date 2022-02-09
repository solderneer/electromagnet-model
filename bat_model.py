class BatteryModel:
    # Duration in seconds please
    def __init__(self, peak, end, duration, output_resistance, isr = 0):
        self.set_params(peak, end, duration, output_resistance, isr)

    def use(self, duration):
        self.v = self.v - duration * self._gradient
        if self.v < self._boundary[1]:
            raise Exception("Battery model exceeds boundaries")

    def reset(self):
        self.v = self._boundary[0]

    def set_params(self, peak, end, duration, output_resistance, isr):
        self.v = peak
        self.isr = isr
        self.output_resistance = output_resistance
        self._gradient = (peak - end) / duration
        self._boundary = (peak, end)
