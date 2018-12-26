import numpy as np


class Baseline(object):
    def __init__(self, data_file):
        self.data = np.genfromtxt(data_file, dtype=float, skip_header=1, delimiter = ',')

    def find_nearest(self, value):
        array = self.data.T[:][0]

        if not isinstance(array, np.ndarray):
            array = np.array(array)

        idx = (np.abs(array - value)).argmin()

        return self.data[idx][1]

    def strokes_from(self, distance):
        return np.interp(distance, self.data.T[:][0], self.data.T[:][1])
