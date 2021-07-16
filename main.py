from cv_module import Digits
from log import LOG
import argparse

def main():
    digits_cls = Digits()
    digits_cls.read_frame(path="dataset/t2.jpg")
    digits_cls.show_frame(time=1000)
    digits_cls.find_numbers()
    digits_cls.show_frame(time=1000)


if __name__ == "__main__":
    main()