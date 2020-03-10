import mahotas


class ZermikeMoments:

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new_val):
        self._radius = new_val

    def __init__(self, radius):
        self.radius = radius

    def describe(self, image):
        return mahotas.features.zernike_moments(image, self.radius)
