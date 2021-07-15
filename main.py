from cv_module import Image, Digits, Detector, Recognition
from log import LOG
import argparse

def main():
    # image_cls = Image()
    # image_cls.set_frame(path="dataset/thermostat.jpg")
    # image_cls.show_frame(time=1000)
    # image_cls.resize_frame()
    # image_cls.show_frame(time=1000)
    digits_cls = Digits()
    digits_cls.set_frame(path="dataset/thermostat.jpg")
    digits_cls.show_frame(time=1000)
    frame = digits_cls.filter()
    digits_cls.show_frame(frame=frame, time=1000)



if __name__ == "__main__":
    
    main()