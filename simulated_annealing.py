#coding=utf-8

import math
import sys
from random import random


def acceptance_probability(old_energy_state, new_energy_state, temperature):
    try:
        return math.exp(
            (old_energy_state-new_energy_state) * 1.0 / temperature)
    except OverflowError:
        return sys.maxint


def simulated_annealing(
        initial_temp=None,
        temp_min=0.000001,
        annealing_factor=0.9,
        iteration_count=100,
        initial_state_function=None,
        neighbour_function=None,
        energy_distance_function=None,
        acceptance_probabability_function=acceptance_probability,
        print_step=False):
    state = initial_state_function()
    current_energy = energy_distance_function(state)
    if initial_temp:
        temp = initial_temp
    else:
        temp = current_energy
    while temp > temp_min:
        i = 0
        if print_step:
            print 'Current energy {0}'.format(current_energy)
            print 'Current temp {0}'.format(temp)
            print 'Current graph {0}'.format(state.edges(labels=False))
            print
        while i < iteration_count:
            neighbour = neighbour_function(state, temp)
            neighbour_energy = energy_distance_function(neighbour)
            acceptance = acceptance_probabability_function(
                current_energy, neighbour_energy, temp)
            if acceptance > random():
                state = neighbour
                current_energy = neighbour_energy
            i += 1
        temp *= annealing_factor

    return (state, current_energy)
