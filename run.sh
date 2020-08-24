#!/bin/sh

# Variables
file_nanowire_str="nanowire-structure.csv"
file_nanowire_vertex="nanowire-vertices.csv"
file_nanowire_matrix="nanowire-matrix.csv"
file_braid_sequence="braid-sequence.csv"
file_particle_position="particle-positions.csv"
file_particle_movement="particle-movements.csv"
file_nanowire_states="nanowire-states.csv"
file_tqc_metrics="tqc-metrics.csv"

# Constructing the Adjacency Matrix for the given Nanowire structure
: > $file_nanowire_vertex
: > $file_nanowire_matrix
python nanowire-graph.py $file_nanowire_str $file_nanowire_vertex $file_nanowire_matrix

# TQC - performing braiding on the Nanowire
echo "Particle,Path" > $file_particle_movement
echo "P1,P2,P3,P4,P5,P6" > $file_nanowire_states
python compiler.py $file_nanowire_str $file_nanowire_vertex $file_nanowire_matrix $file_braid_sequence $file_particle_position $file_particle_movement $file_nanowire_states
