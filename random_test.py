# coding=utf8
import timeit
from random import randint

import simulated_annealing
from sage.all import *
from sage.graphs.generators.random import RandomRegular
from sage.graphs.graph import Graph


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


def initial_graph_function(degree, vertices):
    return lambda: RandomRegular(degree, vertices)


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


if __name__ == '__main__':
    test_data = [
        # Include any regular graph combination
        # [8, 14],
        # [6, 9],
        # [3, 8],
        # [5, 8],
        # [7, 8],
        # [2, 8],
        # [16, 18]

        # Odd r reguler
        # [4, 17],
        # [8, 15],
        # [10, 15],
        # [12, 15]
        # [4, 18],

        # [18, 20]
        [10, 18]
    ]
    iteration_count = 10000

    print test_data

    for conf in test_data:
        degree = conf[0]
        vertex = conf[1]

        print 'degree: %s vertex: %s' % (degree, vertex)

        start = timeit.default_timer()
        ret = simulated_annealing.simulated_annealing(
            initial_temp=2,
            temp_min=0.05,
            initial_state_function=initial_graph_function(degree, vertex),
            neighbour_function=neighbour,
            energy_distance_function=energy_distance_one_based,
            iteration_count=iteration_count,
            # print_step=True
        )
        elapsed = timeit.default_timer() -  start
        # if ret[1] == 0:
        print 'Labels: %s' % ret[0].edges(labels=False)
        print 'Energy diff: %s' % ret[1]
        print 'Time diff: %f' % elapsed
        print 'n === 0 (mod 4) %s' % (vertex % 4 == 0, )
        print 'n === r + 2 === 2 (mod 4) %s' % (
            vertex % (degree + 2) == 0 and
            vertex % 4 == 2 and
            degree % 4 == 0
            , )
        print

        P = ret[0].plot()
        P.show()
