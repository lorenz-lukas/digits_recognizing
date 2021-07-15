from imutils.perspective import four_point_transform
from imutils import contours
import cv2
from log import LOG
from .image import Image

class Digits(Image):

    DIGITS_LOOKUP = {}
    frame = None
    _log = None

    def __init__(self, video=False, path=None):
        self.DIGITS_LOOKUP = {
            (1, 1, 1, 0, 1, 1, 1): 0,
            (0, 0, 1, 0, 0, 1, 0): 1,
            (1, 0, 1, 1, 1, 1, 0): 2,
            (1, 0, 1, 1, 0, 1, 1): 3,
            (0, 1, 1, 1, 0, 1, 0): 4,
            (1, 1, 0, 1, 0, 1, 1): 5,
            (1, 1, 0, 1, 1, 1, 1): 6,
            (1, 0, 1, 0, 0, 1, 0): 7,
            (1, 1, 1, 1, 1, 1, 1): 8,
            (1, 1, 1, 1, 0, 1, 1): 9
        }
        self._log = LOG()
        Image.__init__(self)
    
    def set_frame(self,path=None):
        Image.set_frame(self, path=path)
        Image.resize_frame(self)
        self.frame = Image.get_frame(self)
        
    def filter(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged_frame = cv2.Canny(blurred, 50, 200, 255)
        return edged_frame
