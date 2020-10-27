"""
TQC Braiding Nanowire Algorithm - Validation phase
"""

import utility
import exception

# 1. Nanowire Validation Algorithm which returns a score
def validate_nanowire_state(nanowire,positions,positions_single,voltages,cutoff_pairs,cutoff_pairs_opp,type,msg):
    try:
        min_free_branch = 0
        if type==2:
            min_free_branch = 1
        elif type==1:
            min_free_branch = 2

        score = validate_empty_branches(nanowire,min_free_branch,msg)
        validate_multi_modal_crossing(positions,positions_single,voltages,cutoff_pairs,cutoff_pairs_opp,msg)
        return score
    except exception.InvalidNanowireStateException:
        raise

# 2. Checks if there are at least 2 empty branches in every intersection
def validate_empty_branches(nanowire,min_free_branch,msg):
    score = 0
    valid = False

    for intersection in nanowire:
        free_b = 0
        for branch in intersection:
            min_free_pos = len(branch)
            free_p = 0
            for tup in branch:
                if type(tup) is not dict:
                    continue
                if list(tup.values())[0]==0:
                    free_p += 1
                else:
                    free_p = 0
            if free_p>=min_free_pos:
                free_b += 1
        if free_b>=min_free_branch:
            valid = True

    if valid:
        score += 1
    if score==0:
        raise exception.NoEmptyBranchException(msg)
    return score

# 3. *Check if resulting nanowire violates Rule 3 - Particle-Zero mode isolation
def validate_multi_modal_crossing(positions,positions_single,voltages,cutoff_pairs,cutoff_pairs_opp,msg):
    perm = utility.get_permutations(positions_single,2)
    for pair in perm:
        flag1 = utility.check_particle_pair_zmode(pair,positions,positions_single,None)
        flag2 = verify_cutoff_pair(cutoff_pairs,pair,voltages)
        flag3 = verify_cutoff_pair(cutoff_pairs_opp,pair,voltages)
        if flag1 is False and (flag2 is True or flag3 is True):
            raise exception.MultiModalCrossingException(msg)

# 4. Checks if any other particle blocks the path
def validate_path_particle(path,positions,vertices,par):
    block = []
    for el in path:
        pos = vertices[el]
        if pos in positions:
            block.append(pos)
    block.pop()

    if len(block)>1 and flag:
        route = [vertices[e] for e in path]
        msg = "The Particle ({}) with Path [{}] is blocked in [{}]".format(par,','.join(route),','.join(block))
        raise exception.PathBlockedException(msg)
    return block

# 5. Checks if a shut voltage gate blocks the path
def validate_path_gates(par,path,vertices,voltages,cutoff_pairs,cutoff_pairs_opp):
    p1 = vertices[path[0]]
    pn = vertices[path[len(path)-1]]
    pair = [p1,pn]
    gates = []

    flag1 = verify_cutoff_pair(cutoff_pairs,pair,voltages)
    gate1 = get_voltage_gate_values(flag1)
    if gate1 is not None:
        gates.append(gate1)
    else:
        flag2 = verify_cutoff_pair(cutoff_pairs_opp,pair,voltages)
        gate2 = get_voltage_gate_values(flag2)
        if gate2 is not None:
            gates.append(gate2)

    if flag1>=0 or flag2>=0:
        route = [vertices[e] for e in path]
        msg = "The Particle ({}) with Path [{}] is blocked by Voltage Gate {}".format(par,','.join(route),gates)
        raise exception.PathBlockedException(msg)
    return True

# Returns [0-4] if the pair is in the cutoff_pair
def verify_cutoff_pair(cutoff,pair,voltages):
    flag = -1
    for i in range(len(cutoff)):
        pairs = cutoff[i]
        if pair in pairs or list(reversed(pair)) in pairs:
            if voltages[i] is 'S':
                flag = i
                return flag
    return flag

# For output format
def get_voltage_gate_values(flag):
    gate = None
    if flag is 0:
        gate = 'x11'
    elif flag is 1:
        gate = 'x12'
    elif flag is 2:
        gate = 'x21'
    elif flag is 3:
        gate = 'x22'
    return gate

# 6. Check if the pair is in the same branch
def check_unibranch_validity(pair,positions,intersection):
    check = []
    for par in pair:
        b = 0
        pos = positions[par-1]
        for branch in intersection:
            b +=1
            for tup in branch:
                if type(tup) is not dict:
                    continue
                if list(tup.keys())[0] == pos:
                    check.append(b)
    if check[0]==check[1]:
        return True
    return False