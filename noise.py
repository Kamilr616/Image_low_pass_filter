from numpy import uint8, ones, random, nan, nan_to_num, clip

from cv2 import randn, add, multiply

MEAN = 127
STD_DEV = 32


def _create_nosie(noise_type, mul, size, channels):
    if channels and size and mul:
        if noise_type == 301:
            noise_arr = ones(size, dtype=uint8)
            m = ones(channels, dtype=uint8) * MEAN
            d = ones(channels, dtype=uint8) * STD_DEV
            randn(noise_arr, m, d)
            noise_arr = (noise_arr * mul).astype(uint8)
            return noise_arr
        elif noise_type == 302:
            if mul > 1:
                mul = 1
            noise_arr = ones(size, dtype=uint8)
            intensity_levels = 2 ** (noise_arr[0, 0].nbytes * 8)
            min_intensity = 0
            max_intensity = intensity_levels - 1
            random_image_arr = random.choice([min_intensity, 1, nan], p=[mul / 2, 1 - mul, mul / 2], size=size)
            salt_and_peppered_arr = noise_arr.astype(float) * random_image_arr
            return nan_to_num(salt_and_peppered_arr, nan=max_intensity).astype(uint8)
        elif noise_type == 303:
            pass
        else:
            raise ValueError(f'Unsupported noise type: {noise_type}')
    else:
        raise ValueError('No enough parameters provided')


class Noise:
    def __init__(self, noise_type=301, mul=0.5, size=(256, 256)):
        self._mul = mul
        self._type = noise_type
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
        self._noise = _create_nosie(self._type, self._mul, self._size, self._channels)

    @property
    def channels(self):
        return self._channels

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
        self._noise = _create_nosie(self._type, self._mul, self._size, self._channels)

    @property
    def mul(self):
        return self._mul

    def set_mul(self, value):
        self._mul = float(value)

    def image_noise(self, image):
        self._noise = _create_nosie(self._type, self._mul, self._size, self._channels)
        if self.noise is not None and image is not None:
            noise = self._noise
            if self.type == 301:
                return add(image, noise)
            elif self.type == 302:
                return add(image, noise)
            else:
                raise ValueError(f'Unsupported noise type: {self.type}')
        else:
            raise ValueError("Noise or image not set")

    def _create_default_noise(self):
        return _create_nosie(self._type, self._mul, self._size, self._channels)
