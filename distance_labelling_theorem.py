# coding=utf-8
"""
This file will contains criteria for a graph to have distance magic labelling.
"""
from utils import get_logger

logger = get_logger(__name__)

def get_graph_param(graph):
    """
    Return graph parameter of r regular constant and n vertices constant
    :param graph:
    :return: (r, n)
    """
    return graph.degree(0), len(graph.vertices())


def criteria_1(graph):
    """

    For n even, an r-regular distance magic graph with n vertices exists
    if and only if 2 ≤ r ≤ n − 2, r ≡ 0 (mod 2) and
    either n ≡ 0 (mod 4) or n≡r+2≡2 (mod 4).

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            n % 2 == 0 and
            2 <= r <= n - 2 and r % 2 == 0 and
            (n % 4 == 0 or (n % 4 == 2 and r % 4 == 0))):
        logger.info('Criteria 1')
        return True
    return False


def criteria_2(graph):
    """
    There exists a 4-regular distance magic graph of odd order n
    if and only if n ≥ 17.

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            r == 4 and
            n % 2 == 1 and
            n >= 17):
        logger.info('Criteria 2')
        return True
    return False


def criteria_3(graph):
    """

    There exists a 6-regular distance magic graph of odd order n
    if and only if n = 9 or n ≥ 13.

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            r == 6 and
            n % 2 == 1 and
            (n == 9 or n >= 13)):
        logger.info('Criteria 3')
        return True
    return False


def criteria_4(graph):
    """
    There exists an 8-regular distance magic graph of odd order n
    if and only if n ≥ 15.

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            r == 8 and
            n % 2 == 1 and
            n >= 15):
        logger.info('Criteria 4')
        return True
    return False


def criteria_5(graph):
    """

    There exists a 10-regular distance magic graph of odd order n
    if and only if n ≥ 15.

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            r == 10 and
            n % 2 == 1 and
            n >= 15):
        logger.info('Criteria 5')
        return True
    return False


def criteria_6(graph):
    """

    There exists a 12-regular distance magic graph of odd order n
    if and only if n ≥ 15.

    :param graph:
    :return:
    """
    r, n = get_graph_param(graph)
    if (
            r == 12 and
            n % 2 == 1 and
            n >= 15):
        logger.info('Criteria 6')
        return True
    return False
