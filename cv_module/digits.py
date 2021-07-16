# from typing import tuple
from imutils.perspective import four_point_transform
from imutils import grab_contours
from imutils.contours import sort_contours
import cv2
from log import LOG
from .image import Image

class Digits(Image):

    AREA_PERCENTAGE = 0.5
    DIGITS_LOOKUP = {}
    frame = None
    frame_gray = None
    _log = LOG(__name__)
    _display = None
    _digits = []

    def __init__(self, video=False, path=None) -> None:
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
        Image.__init__(self)
    
    def read_frame(self,path=None) -> None:
        Image.read_frame(self, path=path)
        self.frame = Image.resize_frame(self)
        
    def filter_frame(self, frame=None) -> cv2.CV_64F:
        if(frame is None):
            self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        else:
            self.frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.frame = frame.copy()
        blurred = cv2.GaussianBlur(self.frame_gray, (5, 5), 0)
        edged_frame = cv2.Canny(blurred, 50, 200, 255)
        return edged_frame

    def get_contours(self, edged_frame=None) -> list:
        self._display = []
        cnts = cv2.findContours(edged_frame.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                self._display = approx
                break
        return self._display

    def get_display(self, display=None, frame=None) -> tuple([cv2.CV_64F, cv2.CV_64F]):
        if(type(self._display) is list or type(display) is list):
            self._log.warning("Unable to retrive display!")
            exit(1)
        if(display is None and self._display is not None):
            warped = four_point_transform(self.frame_gray, self._display.reshape(4, 2))
            output = four_point_transform(self.frame, self._display.reshape(4, 2))
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            warped = four_point_transform(gray, display.reshape(4, 2))
            output = four_point_transform(frame, display.reshape(4, 2))
        return warped, output

    def filter_display(self, warped=None) -> cv2.CV_64F:
        thresh = cv2.threshold(warped, 0, 255,
                                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        return thresh

    def get_numbers(self, thresh=None) -> list:
        self._digits = []
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
        for c in cnts:
            (_, _, w, h) = cv2.boundingRect(c)
            if w >= 15 and (h >= 30 and h <= 40):
                self._digits.append(c)
        self._digits = sort_contours(self._digits,
	                                    method="left-to-right")[0]
        return self._digits
    
    def recognize_digits(self, thresh=None, frame=None, digits=None) -> tuple([cv2.CV_64F, list]):
        if (digits is None):
            digits = self._digits
        numbers = []
        for c in self._digits:
            # extract the digit ROI
            (x, y, w, h) = cv2.boundingRect(c)
            roi = thresh[y:y + h, x:x + w]
            # compute the width and height of each of the 7 segments
            # we are going to examine
            (roiH, roiW) = roi.shape
            (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
            dHC = int(roiH * 0.05)
            # define the set of 7 segments
            segments = [
                ((0, 0), (w, dH)),	# top
                ((0, 0), (dW, h // 2)),	# top-left
                ((w - dW, 0), (w, h // 2)),	# top-right
                ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
                ((0, h // 2), (dW, h)),	# bottom-left
                ((w - dW, h // 2), (w, h)),	# bottom-right
                ((0, h - dH), (w, h))	# bottom
            ]
            on = [0] * len(segments)
            # loop over the segments
            for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
                # extract the segment ROI, count the total number of
                # thresholded pixels in the segment, and then compute
                # the area of the segment
                segROI = roi[yA:yB, xA:xB]
                total = cv2.countNonZero(segROI)
                area = (xB - xA) * (yB - yA)
                # if the total number of non-zero pixels is greater than
                # 50% of the area, mark the segment as "on"
                if total / float(area) > self.AREA_PERCENTAGE:
                    on[i]= 1
            # lookup the digit and draw it on the image
            digit = self.DIGITS_LOOKUP[tuple(on)]
            numbers.append(digit)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            self.frame = cv2.putText(frame, str(digit), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        
        self._log.info(u"{}{}.{} \u00b0C".format(*numbers))
        return self.frame, numbers

    def find_numbers(self, frame=None) -> tuple([cv2.CV_64F, list]):
        if(frame is None):
            frame = self.frame.copy()
        edged = self.filter_frame(frame)
        self.get_contours(edged_frame=edged)
        warped, output = self.get_display()
        # (73,115), (224,148)
        thresh = self.filter_display(warped)
        digits = self.get_numbers(thresh=thresh)
        frame, numbers = self.recognize_digits(thresh=thresh, frame=output, digits=digits)
        return frame, numbers


