from numpy import uint8, ones, ceil, prod, random

from cv2 import randn


class Noise:
    def __init__(self, noise_type=1, mean=128, dst=20, mul=0.5, size=(256, 256)):
        self._mul = mul
        self._type = noise_type
        self._mean = mean
        self._dst = dst
        self._size = size
        if len(self._size) == 3:
            self._channels = self._size[2]
        else:
            self._channels = 1
        self._noise = self._create_default_noise()

    @property
    def noise(self):
        return self._noise

    @property
    def size(self):
        return self._size

    def set_size(self, value):
        self._size = value
        if len(self._size) == 3:
            self._channels = self._size[2]
        else:
            self._channels = 1
        self._noise = self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)

    @property
    def channels(self):
        return self._channels
    @property
    def mean(self):
        return self._mean

    def set_mean(self, value):
        self._mean = value
        self._noise = self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)

    @property
    def dst(self):
        return self._dst

    def set_dst(self, value):
        self._dst = value
        self._noise = self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
        self._noise = self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)

    @property
    def mul(self):
        return self._mul

    def set_mul(self, value):
        self._mul = value
        self._noise = self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)

    def _create_nosie(self, noise_type, mean, stddev, mul, size, channels):
        if mean and stddev and size and mul:
            if noise_type == 1:
                gauss_noise = ones(size, dtype=uint8)
                m = ones(channels, dtype=uint8) * mean
                d = ones(channels, dtype=uint8) * stddev
                randn(gauss_noise, m, d)
                gauss_noise = (gauss_noise * mul).astype(uint8)
                return gauss_noise
            elif noise_type == 2:
                pass
            else:
                raise ValueError('Invalid noise type')
        else:
            raise ValueError('No enough parameters provided')

    def _create_default_noise(self):
        return self._create_nosie(self._type, self._mean, self._dst, self._mul, self._size, self._channels)
