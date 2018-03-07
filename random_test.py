# coding=utf8
from random import randint

import simulated_annealing
from distance_labelling_theorem import (
    criteria_1, criteria_2, criteria_3,
    criteria_4, criteria_5, criteria_6)
from sage.all import *
from sage.graphs.generators.random import RandomRegular
from sage.graphs.graph import Graph

import timeit

from utils import get_logger, set_log_level

logger = get_logger(__name__)


def neighbour(graph, temp):
    """
    We got the neighbour of the graph (the variant of regular graph)
    by switching a label.

    :param graph:
    :param temp:
    :return:
    """
    # randomly chose a vertex
    vertices = graph.vertices()
    chosen_vertex = vertices[randint(0, len(vertices) - 1)]
    vertices.remove(chosen_vertex)
    swapped_vertex = vertices[randint(0, len(vertices) - 1)]
    vertices.remove(swapped_vertex)
    edges = graph.edges(labels=False)
    swapped_edges = []
    for e in edges:
        new_e = tuple(
            [
                swapped_vertex if t == chosen_vertex else
                chosen_vertex if t == swapped_vertex else
                t
                for t in e])
        swapped_edges.append(new_e)

    # create new graph
    neighbour_graph = Graph(swapped_edges)
    return neighbour_graph


def initial_graph_function(degree, vertices, seed=None):
    return lambda: RandomRegular(degree, vertices, seed=seed)


def energy_distance(graph):
    """
    We calculate energy distance from a given graphs to the solutions. The smaller the closer to solutions
    :param graph:
    :return:
    """
    # We calculate the distance by calculating the variance of vertex
    # weight to its mean weight, since we want
    # all vertex to have the same weight by magic graph labelling definitions
    weight_sum = 0
    for v in graph.vertices():
        for e in graph.edges():
            if v in e:
                weight_sum += e[1] if v == e[0] else e[0]

    weight_mean = weight_sum / len(graph.vertices())

    # calculate variance of each vertex
    energy_variance = 0
    for v in graph.vertices():
        weight = 0
        for e in graph.edges():
            if v in e:
                weight += e[1] if v == e[0] else e[0]

        energy_variance += (weight - weight_mean) ** 2
    # return the variance as energy distance from the given state to solutions
    return energy_variance


def energy_distance_one_based(graph):
    """
    We calculate energy distance from a given graphs to the solutions. The smaller the closer to solutions
    :param graph:
    :return:
    """
    # We calculate the distance by calculating the variance of vertex weight
    # to its mean weight, since we want
    # all vertex to have the same weight by magic graph labelling definitions
    weight_sum = 0
    for v in graph.vertices():
        for e in graph.edges():
            if v in e:
                weight_sum += e[1] + 1 if v == e[0] else e[0] + 1

    weight_mean = weight_sum / len(graph.vertices())

    # calculate variance of each vertex
    energy_variance = 0
    for v in graph.vertices():
        weight = 0
        for e in graph.edges():
            if v in e:
                weight += e[1] + 1 if v == e[0] else e[0] + 1

        energy_variance += (weight - weight_mean) ** 2
    # return the variance as energy distance from the given state to solutions
    return energy_variance


def generate_regular_graph_param_test_data():
    """

    Generate required R and N combination for test data

    :return:
    """
    graph_params = []
    # Generate even N regular graph
    for n in range(4, 18, 2):
        # Generate even R degree
        for r in range(2, n, 2):
            graph_params.append([r, n])

    # Generate odd N regular graph
    for n in range(9, 19, 2):
        # Generate even R degree
        for r in range(2, n, 2):
            graph_params.append([r, n])
    return graph_params


if __name__ == '__main__':

    # Set log level
    set_log_level(log_level='INFO')

    test_data = [
        # Include any regular graph combination
    ]
    test_data = test_data + generate_regular_graph_param_test_data()
    iteration_count = 100

    logger.info('Test matrix: {0}'.format(test_data))

    # for combination of graph params in test_data:
    for param in test_data:
        r = param[0]
        n = param[1]

        logger.info('degree: {0} vertex: {1}'.format(r, n))

        g = initial_graph_function(r, n)()

        criterias = [
            criteria_1,
            criteria_2,
            criteria_3,
            criteria_4,
            criteria_5,
            criteria_6
        ]
        criteria_found = False
        for crit in criterias:
            if crit(g):
                criteria_found = True
                break
        if not criteria_found:
            logger.info('Distance magic graph not guaranteed to exists.')
            logger.info('Skipping.')
            logger.info('')
            continue

        logger.info('Distance magic graph exists')

        # Proceed only if distance magic graph is guaranteed to exists
        # by the theorem (criteria)

        start_try = timeit.default_timer()

        # Try until it succeeds, because it was guaranteed to exists
        successful_graph = []
        tries = 0
        while True:
            logger.info('Try count: {0}'.format(tries))
            start = timeit.default_timer()
            end_graph, energy_difference = simulated_annealing.simulated_annealing(
                initial_temp=2,
                temp_min=0.05,
                initial_state_function=lambda: g,
                neighbour_function=neighbour,
                energy_distance_function=energy_distance_one_based,
                iteration_count=iteration_count,
            )
            elapsed = timeit.default_timer() - start

            # When distance magic graph is found
            if energy_difference == 0:
                # Try to find another graph
                isomorphic_found = False
                for s in successful_graph:
                    if end_graph.is_isomorphic(s):
                        isomorphic_found = True
                        break

                if isomorphic_found:
                    logger.info(
                        'Graph is isomorphic with previous. Stop trying...')
                    break
                else:
                    # if not isomorphic, remember this graph and find possible
                    # existing alternative in the next loop
                    successful_graph.append(end_graph)

                logger.info('Found distance magic graph.')
                logger.info('Labels: {0}'.format(
                    end_graph.edges(labels=False)
                ))
                logger.info('Annealing time: {0}'.format(elapsed))
            else:
                logger.info('Distance magic graph not found. Retrying...')

            # Found or not, prepare for next iteration
            # randomize new regular graph
            tries += 1
            g = initial_graph_function(r, n)()


        end_try = timeit.default_timer() - start_try
        logger.info('Effort time: {0}'.format(end_try))
        logger.info('')
