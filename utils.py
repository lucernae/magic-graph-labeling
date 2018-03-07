# coding=utf-8

import logging

logger_dict = {}

def get_logger(name, log_level='ERROR'):
    logging.basicConfig()
    if name not in logger_dict:
        logger = logging.getLogger(name)
        logger.setLevel(log_level.upper())
        logger_dict[name] = logger
    else:
        logger = logger_dict[name]
    return logger


def set_log_level(name=None, log_level='ERROR'):
    if name:
        logger = logger_dict['name']
        logger.setLevel(log_level.upper())
    else:
        for k in logger_dict:
            logger = logger_dict[k]
            logger.setLevel(log_level.upper())
