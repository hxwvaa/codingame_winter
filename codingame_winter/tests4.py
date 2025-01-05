
import sys
import math

width, height = [int(i) for i in input().split()]

def print_map(occupied_positions, width, height):
    """Print the map with 1 for occupied and 0 for unoccupied to stderr."""
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in occupied_positions:
                row.append("1")
            else:
                row.append("0")
        sys.stderr.write(" ".join(row) + "\n")

def get_spore_position(protein_pos, occupied_positions, sporer_pos, width, height):
    px, py = protein_pos
    sx, sy = sporer_pos

    directions = {
        'N': [(sx, y) for y in range(sy-1, -1, -1)],
        'S': [(sx, y) for y in range(sy+1, height)],
        'E': [(x, sy) for x in range(sx+1, width)],
        'W': [(x, sy) for x in range(sx-1, -1, -1)]
    }

    best_direction = None
    best_pos = None
    best_distance = float('inf')

    for direction, positions in directions.items():
        for pos in positions:
            if pos in occupied_positions:
                break

            if abs(pos[0] - px) + abs(pos[1] - py) == 2:
                distance = abs(pos[0] - sx) + abs(pos[1] - sy)
                if distance < best_distance:
                    best_distance = distance
                    best_pos = pos
                    best_direction = direction

    return best_pos, best_direction

def get_best_sporer_direction(x, y, proteins):
    """Determine the best direction for a sporer based on protein positions."""
    if not proteins:
        return 'N'
        
    nearest_protein = min(proteins, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
    px, py, _ = nearest_protein
    
    dx = px - x
    dy = py - y
    
    if abs(dx) > abs(dy):
        return 'E' if dx > 0 else 'W'
    else:
        return 'S' if dy > 0 else 'N'

def find_nearest_unharvested_protein(pos, proteins, my_organs):
    """Find the nearest protein that isn't being harvested."""
    best_distance = float('inf')
    best_protein = None
    
    for px, py, p_type in proteins:
        # Check if protein is already being harvested
        is_harvested = any(abs(org_x - px) + abs(org_y - py) == 1 
                          for org_x, org_y, _, _, _ in my_organs)
        
        if not is_harvested:
            distance = abs(pos[0] - px) + abs(pos[1] - py)
            if distance < best_distance:
                best_distance = distance
                best_protein = (px, py, p_type)
    
    return best_protein, best_distance

def find_best_growth_position(my_organs, proteins, occupied_positions):
    """Find the best organ and position to grow from, prioritizing positions near proteins."""
    best_score = float('inf')
    best_growth = None
    
    # First, try to find positions adjacent to proteins
    for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
        possible_positions = [
            (organ_x + 1, organ_y),
            (organ_x - 1, organ_y),
            (organ_x, organ_y + 1),
            (organ_x, organ_y - 1)
        ]
        
        for new_x, new_y in possible_positions:
            if (new_x, new_y) not in occupied_positions:
                # Find nearest unharvested protein
                nearest_protein, distance = find_nearest_unharvested_protein(
                    (new_x, new_y), proteins, my_organs)
                
                if nearest_protein:
                    px, py, _ = nearest_protein
                    score = distance
                    
                    # Strongly prioritize positions that would be adjacent to proteins
                    if distance == 1:
                        score -= 1000
                    
                    # Prioritize positions that move toward proteins
                    if abs(new_x - px) + abs(new_y - py) < abs(organ_x - px) + abs(organ_y - py):
                        score -= 50
                        
                    if score < best_score:
                        best_score = score
                        if distance == 1:  # Adjacent to protein
                            # Determine direction for harvester
                            if new_x == px and new_y < py:
                                direction = 'S'
                            elif new_x == px and new_y > py:
                                direction = 'N'
                            elif new_y == py and new_x < px:
                                direction = 'E'
                            else:
                                direction = 'W'
                            best_growth = (organ_id, new_x, new_y, "HARVESTER", direction)
                        else:  # Moving toward protein
                            best_growth = (organ_id, new_x, new_y, "BASIC", "N")
    
    return best_growth

while True:
    proteins = []
    my_organs = []
    my_sporers = []
    enemy_organs = []
    occupied_positions = set()
    
    entity_count = int(input())
    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])
        type_ = inputs[2]
        owner = int(inputs[3])
        organ_id = int(inputs[4])
        organ_dir = inputs[5]
        
        occupied_positions.add((x, y))
        
        if owner == 1:
            my_organs.append((x, y, organ_id, type_, organ_dir))
            if type_ == "SPORER":
                my_sporers.append((x, y, organ_id, organ_dir))
        elif owner == 0:
            enemy_organs.append((x, y, type_))
                
        if type_ in ['A', 'B', 'C', 'D']:
            proteins.append((x, y, type_))
    
    sys.stderr.write("Occupied Positions Map:\n")
    print_map(occupied_positions, width, height)
    
    print(f"Proteins: {proteins}", file=sys.stderr)
    print(f"My Organs: {my_organs}", file=sys.stderr)
    print(f"My Sporers: {my_sporers}", file=sys.stderr)
    
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())

    ####################################################################################################
    # used_organs = set()  # Track organs used for growth in the current turn

    # def get_next_action():
    #     global used_organs
        
    #     if not my_organs:
    #         return "WAIT"
        
    #     # First priority: Use SPORER if available and resources are sufficient
    #     if my_sporers and my_a >= 1 and my_b >= 1 and my_c >= 1 and my_d >= 1:
    #         sporer_x, sporer_y, sporer_id, sporer_dir = my_sporers[0]
    #         for px, py, _ in proteins:
    #             is_harvested = any(abs(org_x - px) + abs(org_y - py) == 1 
    #                             for org_x, org_y, _, _, _ in my_organs)
                
    #             if not is_harvested:
    #                 spore_result = get_spore_position((px, py), occupied_positions, (sporer_x, sporer_y), width, height)
    #                 if spore_result:
    #                     spore_pos, needed_direction = spore_result
    #                     if sporer_dir == needed_direction:
    #                         return f"SPORE {sporer_id} {spore_pos[0]} {spore_pos[1]}"
        
    #     # Second priority: Grow a SPORER if resources allow
    #     if not my_sporers and my_b >= 1 and my_d >= 1:
    #         best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
    #         if best_growth:
    #             organ_id, x, y, _, _ = best_growth
    #             if organ_id not in used_organs:
    #                 best_direction = get_best_sporer_direction(x, y, proteins)
    #                 used_organs.add(organ_id)
    #                 return f"GROW {organ_id} {x} {y} SPORER {best_direction}"
        
    #     # Third priority: Grow harvesters and expand
    #     best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
    #     if best_growth:
    #         organ_id, x, y, type_, direction = best_growth
    #         if organ_id not in used_organs:
    #             if type_ == "HARVESTER" and my_c >= 1 and my_d >= 1:
    #                 used_organs.add(organ_id)
    #                 return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
    #             elif type_ == "BASIC" and my_a >= 1:
    #                 used_organs.add(organ_id)
    #                 return f"GROW {organ_id} {x} {y} BASIC N"
        
    #     # Fallback: Grow a basic organ if no other action is possible
    #     for organ_x, organ_y, organ_id, _, _ in my_organs:
    #         if organ_id not in used_organs:
    #             possible_positions = [
    #                 (organ_x + 1, organ_y),
    #                 (organ_x - 1, organ_y),
    #                 (organ_x, organ_y + 1),
    #                 (organ_x, organ_y - 1)
    #             ]
    #             for new_x, new_y in possible_positions:
    #                 if (new_x, new_y) not in occupied_positions and my_a >= 1:
    #                     used_organs.add(organ_id)
    #                     return f"GROW {organ_id} {new_x} {new_y} BASIC N"
        
    #     return "WAIT"

    used_organs = set()  # Track organs used for growth in the current turn
    used_roots = set()  # Track which ROOTs have been used for growth

    def get_next_action():
        global used_organs, used_roots
        
        if not my_organs:
            return "WAIT"
        
        # First priority: Use SPORER if available and resources are sufficient
        if my_sporers and my_a >= 1 and my_b >= 1 and my_c >= 1 and my_d >= 1:
            sporer_x, sporer_y, sporer_id, sporer_dir = my_sporers[0]
            for px, py, _ in proteins:
                is_harvested = any(abs(org_x - px) + abs(org_y - py) == 1 
                                for org_x, org_y, _, _, _ in my_organs)
                
                if not is_harvested:
                    spore_result = get_spore_position((px, py), occupied_positions, (sporer_x, sporer_y), width, height)
                    if spore_result:
                        spore_pos, needed_direction = spore_result
                        if sporer_dir == needed_direction:
                            return f"SPORE {sporer_id} {spore_pos[0]} {spore_pos[1]}"
        
        # Second priority: Grow a SPORER if resources allow
        if not my_sporers and my_b >= 1 and my_d >= 1:
            best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
            if best_growth:
                organ_id, x, y, _, root_id = best_growth  # Include root_id
                if organ_id not in used_organs and root_id not in used_roots:
                    best_direction = get_best_sporer_direction(x, y, proteins)
                    used_organs.add(organ_id)
                    used_roots.add(root_id)  # Mark the ROOT as used
                    return f"GROW {organ_id} {x} {y} SPORER {best_direction}"
        
        # Third priority: Grow harvesters and expand
        best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
        if best_growth:
            organ_id, x, y, type_, root_id = best_growth  # Include root_id
            if organ_id not in used_organs and root_id not in used_roots:
                if type_ == "HARVESTER" and my_c >= 1 and my_d >= 1:
                    # Determine direction for the HARVESTER
                    if x == proteins[0][0] and y < proteins[0][1]:
                        direction = 'S'
                    elif x == proteins[0][0] and y > proteins[0][1]:
                        direction = 'N'
                    elif y == proteins[0][1] and x < proteins[0][0]:
                        direction = 'E'
                    else:
                        direction = 'W'
                    
                    used_organs.add(organ_id)
                    used_roots.add(root_id)  # Mark the ROOT as used
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif type_ == "BASIC" and my_a >= 1:
                    direction = 'N'  # Default direction for BASIC organ
                    used_organs.add(organ_id)
                    used_roots.add(root_id)  # Mark the ROOT as used
                    return f"GROW {organ_id} {x} {y} BASIC {direction}"
        
        # Fallback: Grow a basic organ if no other action is possible
        for organ_x, organ_y, organ_id, _, root_id in my_organs:  # Include root_id
            if organ_id not in used_organs and root_id not in used_roots:
                possible_positions = [
                    (organ_x + 1, organ_y),
                    (organ_x - 1, organ_y),
                    (organ_x, organ_y + 1),
                    (organ_x, organ_y - 1)
                ]
                for new_x, new_y in possible_positions:
                    if (new_x, new_y) not in occupied_positions and my_a >= 1:
                        used_organs.add(organ_id)
                        used_roots.add(root_id)  # Mark the ROOT as used
                        return f"GROW {organ_id} {new_x} {new_y} BASIC N"
        
        return "WAIT"




    # Reset used organs set at the start of each turn
    used_organs.clear()
    for _ in range(required_actions_count):
        action = get_next_action()
        print(action)
        
        # Update occupied positions and track growth
        if action != "WAIT":
            if action.startswith("SPORE"):
                _, _, x, y = action.split()
                occupied_positions.add((int(x), int(y)))
            elif action.startswith("GROW"):
                _, _, x, y, *_ = action.split()
                occupied_positions.add((int(x), int(y)))
