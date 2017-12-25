# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import logging


def get_logger(logger_name=None):
    from logging import getLogger
    if not logger_name:
        logger_name = "push7_cmd"

    return getLogger(logger_name)


def _init_logger():
    logger = get_logger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)-4d: %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


_init_logger()

