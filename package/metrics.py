"""
License:
    Copyright (C) 2020
    All rights reserved.
    Arahant Ashok Kumar (aak700@nyu.edu)

Module: Metrics

Objectives: Generates outputs

Functions:
    1. update_particle_movements
    2. update_nanowire_state
    3. update_particle_line_positions
    4. update_final_particle_positions
"""

import copy

def update_particle_movements(file, pair, par, path, vertices, voltages):
    """
    Update Particle positions by generating a similar sequence for the particles.
    """
    try:
        fw = open(file, 'a')
        line = "{},{},{},{}".format(str(pair[0]), str(pair[1]), par,
                                    '-'.join(vertices[v] for v in path))
        line = "{},{}".format(line, ','.join(voltages))
        fw.write(line+'\n')
        fw.close()
        print(line)
    except IOError as err:
        print(err)

def update_nanowire_state(file, pair, positions, path, vertices, par, voltages):
    """
    Update Nanowire state matrix
    """
    try:
        fw = open(file, 'a')
        for p in path:
            pos_temp = copy.copy(positions)
            pos = vertices[p]
            # if pos == 'x1' or pos == 'x2':
                # continue
            pos_temp[par-1] = pos
            line = "{},{},{}".format(str(pair[0]), str(pair[1]), ','.join(pos_temp))
            line = "{},{}".format(line, ','.join(voltages))
            fw.write(line+'\n')
        fw.close()
    except IOError as err:
        print(err)

def update_particle_line_positions(file, pair, positions):
    """
    Update Braid particles positions
    """
    try:
        fw = open(file, 'a')
        newpos = [str(e) for e in positions]
        line = "{},{},{}".format(str(pair[0]), str(pair[1]), ','.join(newpos))
        fw.write(line+'\n')
        fw.close()
    except IOError as err:
        print(err)

def update_final_particle_positions(file, positions):
    """
    Update Final particle positions
    """
    try:
        fw = open(file, 'a')
        line = ','.join(positions)
        fw.write(line+'\n')
        fw.close()
    except IOError as err:
        print(err)
