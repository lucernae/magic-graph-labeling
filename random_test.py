#!/usr/local/bin/sage -python
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
        [2, 8]
    ]
    max_vertices = 20
    iteration_count = 10000
    # for i in range(4, max_vertices):
    #     vertex = i
    #     for j in range(2, i-1, 2):
    #         degree = j
    #         test_data.append([degree, vertex])

    for conf in test_data:
        degree = conf[0]
        vertex = conf[1]
        ret = simulated_annealing.simulated_annealing(
            initial_state_function=initial_graph_function(degree, vertex),
            neighbour_function=neighbour,
            energy_distance_function=energy_distance,
            iteration_count=iteration_count
        )
        # if ret[1] == 0:
        print 'degree: %s vertex: %s' % (degree, vertex)
        print 'Labels: %s' % ret[0].edges(labels=False)
        print 'Energy diff: %s' % ret[1]
