from numpy import ones, sum, uint8, outer


from cv2 import getStructuringElement, MORPH_CROSS, MORPH_RECT, MORPH_ELLIPSE, getGaussianKernel


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
        self._kernel = self._create_kernel(self._type, self._size)

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        self._type = value
        self._kernel = self._create_kernel(self._type, self._size)

    @property
    def kernel(self):
        return self._kernel

    def _create_kernel(self, kernel_type, size):
        if size:
            if kernel_type == 102:
                new_kernel = getStructuringElement(MORPH_RECT, (size, size)).astype(uint8)
                return new_kernel / sum(new_kernel)
            if kernel_type == 105:
                new_kernel = getStructuringElement(MORPH_CROSS, (size, size)).astype(uint8)
                return new_kernel / sum(new_kernel)
            elif kernel_type == 106:
                new_kernel = getStructuringElement(MORPH_ELLIPSE, (size, size)).astype(uint8)
                return new_kernel / sum(new_kernel)
            elif kernel_type == 107:
                new_kernel = ones((size, size)).astype(uint8)
                new_kernel[0, 0] = 0
                new_kernel[0, -1] = 0
                new_kernel[-1, 0] = 0
                new_kernel[-1, -1] = 0
                return new_kernel / sum(new_kernel)
            elif kernel_type == 101:
                return None
            elif kernel_type == 103:
                new_kernel = getGaussianKernel(size, 0)
                return outer(new_kernel, new_kernel.transpose())
            else:
                raise ValueError('Invalid kernel type')
        else:
            raise ValueError('No size provided')

    def _create_default_kernel(self):
        return self._create_kernel(self._type, self._size)
