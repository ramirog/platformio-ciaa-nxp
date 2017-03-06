
from platformio.managers.platform import PlatformBase


class CiaanxpPlatform(PlatformBase):

    def is_embedded(self):
        return True

