import numpy as np

class LPF():
    def __init__(self):
        self.meas = []
        self.mean = 0

    def low_pass_filter(self, data, size, alpha):
        self.meas.append(data)
        self.mean = np.mean(self.meas)

        if len(self.meas) > size:
            self.meas.pop(0)
            self.mean = np.mean(self.meas)

        filter_mean = alpha * self.mean + (1-alpha) * self.meas[-1]

        return filter_mean