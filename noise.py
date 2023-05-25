from numpy import uint8, ones, random, nan, nan_to_num

from cv2 import randn, add, multiply

MEAN = 128
STD_DEV = 20


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
        self._noise = self._create_nosie(self._type, self._mul, self._size, self._channels)

    @property
    def channels(self):
        return self._channels

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
        self._noise = self._create_nosie(self._type, self._mul, self._size, self._channels)

    @property
    def mul(self):
        return self._mul

    def set_mul(self, value):
        self._mul = float(value)

    def image_noise(self, image):
        self._noise = self._create_nosie(self._type, self._mul, self._size, self._channels)
        if self.noise is not None and image is not None:
            if self.type == 301:
                return add(image, self._noise)
            elif self.type == 302:
                return multiply(image, self._noise)
            else:
                raise ValueError(f'Unsupported noise type: {self.type}')
        else:
            raise ValueError("Noise or image not set")

    def _create_nosie(self, noise_type, mul, size, channels):
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
                # Derive the number of intensity levels from the array datatype.
                intensity_levels = 2 ** (noise_arr[0, 0].nbytes * 8)
                min_intensity = 0
                max_intensity = intensity_levels - 1
                # Generate an array with the same shape as the image's:
                # Each entry will have:
                # 1 with probability: 1 - prob
                # 0 or np.nan (50% each) with probability: prob
                random_image_arr = random.choice([min_intensity, 1, nan], p=[mul / 2, 1 - mul, mul / 2], size=size)
                # This results in an image array with the following properties:
                # - With probability 1 - prob: the pixel KEEPS ITS VALUE (it was multiplied by 1)
                # - With probability prob/2: the pixel has value zero (it was multiplied by 0)
                # - With probability prob/2: the pixel has value np.nan (it was multiplied by np.nan)
                # We need to to `arr.astype(np.float)` to make sure np.nan is a valid value.
                salt_and_peppered_arr = noise_arr.astype(float) * random_image_arr
                # Since we want SALT instead of NaN, we replace it.
                # We cast the array back to its original dtype so we can pass it to PIL.
                return nan_to_num(salt_and_peppered_arr, nan=max_intensity).astype(uint8)
            elif noise_type == 303:
                pass
            else:
                raise ValueError(f'Unsupported noise type: {noise_type}')
        else:
            raise ValueError('No enough parameters provided')

    def _create_default_noise(self):
        return self._create_nosie(self._type, self._mul, self._size, self._channels)
