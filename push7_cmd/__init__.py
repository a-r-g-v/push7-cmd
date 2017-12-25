# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import logging


def get_logger():
    return logging.getLogger(__name__)


def _init_logger():
    logger = get_logger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)-4d: %(message)s'
    )

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


_init_logger()

