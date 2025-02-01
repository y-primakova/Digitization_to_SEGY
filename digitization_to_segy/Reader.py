import numpy as np
import segyio
from matplotlib import image as mpimg


class Reader:
    @staticmethod
    def read_segy(path):
        segy = segyio.open(path, "r", ignore_geometry=True)
        data = np.array([segy.trace[i] for i in range(segy.tracecount)]).T
        return data

    @staticmethod
    def read_png(path):
        img = mpimg.imread(path)
        image = img[:, :, :3]
        return image

    @staticmethod
    def read_jpeg(path):
        img = mpimg.imread(path, format='jpeg')
        image = img[:, :, :3]
        return image