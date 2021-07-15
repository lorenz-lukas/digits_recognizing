import cv2
from log import LOG
from imutils import resize

class Image:

    frame = None
    __log = LOG(__name__)
    cap = None

    def __init__(self, video=False, path=None):
        if(video == True and path == None):
            self.cap = cv2.VideoCapture(0)
            if(not self.cap.isOpened()):
                self.__log.error("Unable to open Camera!")
                exit(1)

        elif(video == True and path is not None):
            self.cap = cv2.VideoCapture(path)
    
    def get_frame(self):
        return self.frame

    def set_frame(self, video=False, path=None) -> cv2.CV_64F:

        if(video == True):
            ret, self.frame = self.cap.read()
            if(not ret):
                self.__log.warning("End of Video Stream! Exiting ...")
                exit(1)
        else:
            self.frame = cv2.imread(path)

        return self.frame
    
    def show_frame(self, frame=None, window_name="frame", time=33):
        if(frame is None):
            cv2.imshow(window_name, self.get_frame())
        else:
            cv2.imshow(window_name, frame)    
        key = cv2.waitKey(time)
        return key

    def resize_frame(self, h=500, w=500):
        self.frame = resize(self.frame, height=h, width=w)