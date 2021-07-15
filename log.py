#!/usr/bin/env python3
import logging
import colorama
from inspect import stack

class LOG:


    _logger = None
    _ch = None
    init = None


    def __init__(self, file_name = None):
        formatter = logging.Formatter("{}%(asctime)s {}[%(levelname)s] {}[%(name)s]: {}%(message)s".format(
                colorama.Fore.BLUE, colorama.Fore.GREEN, colorama.Fore.CYAN, colorama.Fore.WHITE
            ))
        # create logger
        _stack = stack()[1]
        self._logger = logging.getLogger(_stack[3])
        self._logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        self._ch = logging.StreamHandler()
        self._ch.setLevel(logging.DEBUG)
        self._ch.setFormatter(formatter)
        # add ch to logger
        self._logger.addHandler(self._ch)
        
    def info(self, msg = None):
        formatter = logging.Formatter("{}%(asctime)s {}[%(levelname)s] {}[%(name)s]: {}%(message)s".format(
                colorama.Fore.BLUE, colorama.Fore.GREEN, colorama.Fore.CYAN, colorama.Fore.WHITE
            ))
        self._ch.setFormatter(formatter)
        self._logger.addHandler(self._ch)
        self._logger.info(msg)
        self._logger.removeHandler(self._ch)

    def warning(self, msg = None):
        formatter = logging.Formatter("{}%(asctime)s {}[%(levelname)s] {}[%(name)s]: {}%(message)s".format(
                colorama.Fore.BLUE, colorama.Fore.YELLOW, colorama.Fore.CYAN, colorama.Fore.WHITE
            ))
        self._ch.setFormatter(formatter)
        self._logger.addHandler(self._ch)
        self._logger.warning(msg)
        self._logger.removeHandler(self._ch)

    def error(self, msg = None):
        formatter = logging.Formatter("{}%(asctime)s {}[%(levelname)s] {}[%(name)s]: {}%(message)s".format(
                colorama.Fore.BLUE, colorama.Fore.RED, colorama.Fore.CYAN, colorama.Fore.WHITE
            ))
        self._ch.setFormatter(formatter)
        self._logger.addHandler(self._ch)
        self._logger.error(msg)
        self._logger.removeHandler(self._ch)

    def critical(self, msg = None):
        formatter = logging.Formatter("{}%(asctime)s {}[%(levelname)s] {}[%(name)s]: {}%(message)s".format(
                colorama.Fore.BLUE, colorama.Fore.LIGHTRED_EX, colorama.Fore.CYAN, colorama.Fore.WHITE
            ))
        self._ch.setFormatter(formatter)
        self._logger.addHandler(self._ch)
        self._logger.critical(msg)
        self._logger.removeHandler(self._ch)