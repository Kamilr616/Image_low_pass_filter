from numpy import ones, sum, uint8, outer

from cv2 import getStructuringElement, MORPH_CROSS, MORPH_RECT, MORPH_ELLIPSE, getGaussianKernel, multiply


def _create_kernel(kernel_type, size):
    if size:
        if kernel_type == 102:
            return getStructuringElement(MORPH_RECT, (size, size))
        if kernel_type == 105:
            return getStructuringElement(MORPH_CROSS, (size, size))
        elif kernel_type == 106:
            return getStructuringElement(MORPH_ELLIPSE, (size, size))
        elif kernel_type == 107:
            new_kernel = ones((size, size)).astype(uint8)
            new_kernel[0, 0] = 0
            new_kernel[0, -1] = 0
            new_kernel[-1, 0] = 0
            new_kernel[-1, -1] = 0
            return new_kernel
        elif kernel_type == 101:
            return ones((size, size)).astype(uint8)
        elif kernel_type == 103:
            new_kernel = getGaussianKernel(size, 0)
            return outer(new_kernel, new_kernel.transpose())
        else:
            raise ValueError('Invalid kernel type')
    else:
        raise ValueError('No size provided')


class Kernel:
    def __init__(self, size=3, kernel_type=102):
        self._size = size
        self._type = kernel_type
        self._kernel = self._create_default_kernel()

    @property
    def size(self):
        return self._size

    def set_size(self, value):
        self._size = value
        self._kernel = _create_kernel(self._type, self._size)

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
        self._kernel = _create_kernel(self._type, self._size)

    @property
    def kernel(self):
        return self._kernel

    def get_real_kernel(self):
        if self._type:
            if self._type == 101:
                return self._kernel
            elif self._type == 103:
                return outer(self._kernel, self._kernel.transpose())
            else:
                return self._kernel / sum(self._kernel)
        else:
            raise ValueError('No kernel type')

    def get_teo_kernel(self):
        if self._type:
            if self._type == 103:
                return self._kernel * self._size ** 2
            else:
                return self._kernel
        else:
            raise ValueError('No kernel type')

    def _create_default_kernel(self):
        return _create_kernel(self._type, self._size)
