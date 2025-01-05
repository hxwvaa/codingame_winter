import sys
import math

width, height = [int(i) for i in input().split()]

def find_harvest_target(my_organs, protein_positions):
    """Find the closest harvestable protein."""
    for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
        for px, py in protein_positions:
            if abs(organ_x - px) + abs(organ_y - py) == 1:  # Adjacent protein
                return organ_id, px, py
    return None, None, None

def find_enemy_nearby(my_organs, enemy_organs):
    """Find the closest enemy organ to any of my organs."""
    for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
        for ex, ey, e_type in enemy_organs:
            if abs(organ_x - ex) + abs(organ_y - ey) == 1:  # Adjacent enemy
                return organ_id, ex, ey
    return None, None, None

def find_best_expansion(my_organs, occupied_positions):
    """Find the best organ and position to expand to, avoiding walls and invalid coordinates."""
    for organ_x, organ_y, organ_id, _, _ in my_organs:
        possible_positions = [
            (organ_x + 1, organ_y),
            (organ_x - 1, organ_y),
            (organ_x, organ_y + 1),
            (organ_x, organ_y - 1)
        ]

        # Filter valid positions
        valid_positions = [
            (new_x, new_y) for new_x, new_y in possible_positions
            if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in occupied_positions
        ]

        if valid_positions:
            return organ_id, valid_positions[0][0], valid_positions[0][1]
    return None


def print_map(occupied_positions, width, height):
    """Print the map with 1 for occupied and 0 for unoccupied to stderr, flipped vertically and horizontally."""
    flipped_map = []
    
    for y in range(height):
        row = []
        for x in range(width):
            if (x, y) in occupied_positions:
                row.append("1")
            else:
                row.append("0")
        flipped_map.append(row)

    # Flip the map vertically by reversing the rows
    flipped_map.reverse()  # Reverse the rows

    # Flip each row horizontally by reversing its elements
    for row in flipped_map:
        row.reverse()  # Reverse each row's elements

    # Print the flipped map
    for row in flipped_map:
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
    best_score = float('inf')
    best_growth = None

    for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
        possible_positions = [
            (organ_x + 1, organ_y),
            (organ_x - 1, organ_y),
            (organ_x, organ_y + 1),
            (organ_x, organ_y - 1)
        ]

        # First try empty positions
        valid_positions = [
            (new_x, new_y) for new_x, new_y in possible_positions
            if 0 <= new_x < width and 0 <= new_y < height and 
            (new_x, new_y) not in occupied_positions
        ]

        # If no empty positions, allow protein positions
        if not valid_positions:
            valid_positions = [
                (new_x, new_y) for new_x, new_y in possible_positions
                if 0 <= new_x < width and 0 <= new_y < height and 
                (new_x, new_y) in {(p[0], p[1]) for p in proteins}
            ]

        for new_x, new_y in valid_positions:
            nearest_protein, distance = find_nearest_unharvested_protein(
                (new_x, new_y), proteins, my_organs)

            if nearest_protein:
                px, py, _ = nearest_protein
                score = distance

                if distance == 1:  # Adjacent to protein
                    score -= 1000
                elif abs(new_x - px) + abs(new_y - py) < abs(organ_x - px) + abs(organ_y - py):
                    score -= 50

                if score < best_score:
                    best_score = score
                    if distance == 1:  # Adjacent to protein
                        direction = get_harvester_direction(new_x, new_y, px, py)
                        best_growth = (organ_id, new_x, new_y, "HARVESTER", direction)
                    else:
                        best_growth = (organ_id, new_x, new_y, "BASIC", None)
        if (best_growth):
            orig, new_x, new_y, type_, direction = best_growth
            if (new_x, new_y) in occupied_positions:
                continue

    return best_growth

def get_harvester_direction(x, y, px, py):
    """Determine harvester direction based on protein position."""
    if x == px:
        return 'S' if py > y else 'N'
    return 'E' if px > x else 'W'

def try_to_kill_enemy_tentacle():
    # Loop through all your organs
    for organ_x, organ_y, organ_id, _, _ in my_organs:
        # Loop through all enemy tentacles
        for ex, ey, _ in enemy_tentacles:
            # Check if the enemy tentacle is adjacent to your organ
            possible_attack_positions = [
                (ex + 1, ey, 'W'), (ex - 1, ey, 'E'),
                (ex, ey + 1, 'N'), (ex, ey - 1, 'S')
            ]
            
            for ax, ay, dir_ in possible_attack_positions:
                # If the organ is 1 block away from the enemy tentacle
                if abs(ax - organ_x) + abs(ay - organ_y) == 1:
                    # Check if the position is not occupied by any of the enemy organs or tentacles
                    if (ax, ay) not in occupied_positions:
                        # Ensure you have enough resources to grow a tentacle
                        if my_b >= 1 and my_c >= 1:
                            # Mark the position as occupied and grow a tentacle to attack the enemy
                            occupied_positions.add((ax, ay))
                            return f"GROW {organ_id} {ax} {ay} TENTACLE {dir_}"
    return None

def grow_on_protein_if_possible(my_organs, proteins, occupied_positions, my_a, my_b, my_c, my_d):
    """Grow an organ on a protein if it's not being harvested and adjacent to one of my organs."""
    for organ_x, organ_y, organ_id, _, _ in my_organs:
        for px, py, p_type in proteins:
            # Check if the protein is adjacent to an organ and not being harvested
            if abs(organ_x - px) + abs(organ_y - py) == 1:  # Adjacent protein
                # Check if the protein is already being harvested
                is_harvested = any(abs(org_x - px) + abs(org_y - py) == 1 
                                   for org_x, org_y, _, _, _ in my_organs)
                
                if not is_harvested:
                    # Try to grow an organ on the protein
                    if my_b >= 1 and my_c >= 1:
                        direction = get_harvester_direction(organ_x, organ_y, px, py)
                        occupied_positions.add((px, py))
                        return f"GROW {organ_id} {px} {py} TENTACLE {direction}"

                    elif my_b >= 1 and my_d >= 1:
                        direction = get_best_sporer_direction(organ_x, organ_y, proteins)
                        occupied_positions.add((px, py))
                        return f"GROW {organ_id} {px} {py} SPORER {direction}"

                    elif my_a >= 1:
                        occupied_positions.add((px, py))
                        return f"GROW {organ_id} {px} {py} BASIC"
    return None

def get_next_action():
    global used_organs, used_roots
    
    # Initialize enemy occupied positions
    enemy_occupied_positions = set()
    
    # Add positions of enemy organs and tentacles to the occupied positions
    for ex, ey, _ in enemy_organs:
        enemy_occupied_positions.add((ex, ey))
    for ex, ey, organ_dir in enemy_tentacles:  # Assuming you have a list for enemy tentacles
        enemy_occupied_positions.add((ex, ey))
    
    if not my_organs:
        return "WAIT"
    
    # Check if there's a protein adjacent to an organ and not being harvested
    grow_action = grow_on_protein_if_possible(my_organs, proteins, occupied_positions, my_a, my_b, my_c, my_d)
    if grow_action:
        return grow_action
    
    # Continue with the rest of your logic if no action is taken
    # (Attack, Expand, etc.)

    return "WAIT"


while True:
    enemy_tentacles = []
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
            if type_ == "TENTACLE":  # Assuming TENTACLE is the type for enemy tentacles
                enemy_tentacles.append((x, y, organ_dir))  # Store the tentacle positions
                occupied_positions.add((x, y))
                # Determine the position the tentacle is facing
                if organ_dir == "N":
                    occupied_positions.add((x, y - 1))
                elif organ_dir == "S":
                    occupied_positions.add((x, y + 1))
                elif organ_dir == "E":
                    occupied_positions.add((x + 1, y))
                elif organ_dir == "W":
                    occupied_positions.add((x - 1, y))


                
        if type_ in ['A', 'B', 'C', 'D']:
            proteins.append((x, y, type_))
    
    sys.stderr.write("Occupied Positions Map:\n")
    
    print(f"Proteins: {proteins}", file=sys.stderr)
    print(f"My Organs: {my_organs}", file=sys.stderr)
    print(f"My Sporers: {my_sporers}", file=sys.stderr)
    print(f"enemy tentacles: {enemy_tentacles}", file=sys.stderr)
    
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())

    used_organs = set()  # Track organs used for growth in the current turn
    used_roots = set()  # Track which ROOTs have been used for growth

    def get_next_action():
        global used_organs, used_roots
        
        # Initialize enemy occupied positions
        enemy_occupied_positions = set()
        
        # Add positions of enemy organs and tentacles to the occupied positions
        for ex, ey, _ in enemy_organs:
            enemy_occupied_positions.add((ex, ey))
        for ex, ey, organ_dir in enemy_tentacles:  # Assuming you have a list for enemy tentacles
            enemy_occupied_positions.add((ex, ey))
        
        if not my_organs:
            return "WAIT"
        
        grow_action = grow_on_protein_if_possible(my_organs, proteins, occupied_positions, my_a, my_b, my_c, my_d)
        if grow_action:
            return grow_action


        # First priority: Tentacle growth from any organ if an enemy is 1 block away
        should_attack = False
        attack_x, attack_y, attack_dir = None, None, None
        
        if my_b >= 1 and my_c >= 1:
            # Loop through all organs to check if any organ is 1 block away from the enemy
            for organ_x, organ_y, organ_id, _, _ in my_organs:
                for ex, ey, _ in enemy_organs:
                    # Check if we can place a tentacle next to the enemy
                    possible_attack_positions = [
                        (ex + 1, ey, 'W'), (ex - 1, ey, 'E'),
                        (ex, ey + 1, 'N'), (ex, ey - 1, 'S')
                    ]
                    
                    for ax, ay, dir_ in possible_attack_positions:
                        # If the organ is 1 block away from the enemy
                        if abs(ax - organ_x) + abs(ay - organ_y) == 1:
                            # Check if the position is not occupied by any of the enemy organs or tentacles
                            if (ax, ay) not in occupied_positions and (ax, ay) not in enemy_occupied_positions:
                                if my_b >= 1 and my_c >= 1:
                                    attack_x, attack_y = ax, ay
                                    attack_dir = dir_
                                    should_attack = True
                                    break
                        if should_attack:
                            break
                    
                    if should_attack:
                        # Mark the position as occupied
                        occupied_positions.add((attack_x, attack_y))
                        return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"
        
        # Second priority: Check if there's a protein between an organ and an enemy
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, _, _ in my_organs:
                for ex, ey, _ in enemy_organs:
                    # Check for proteins in between the organ and the enemy
                    if abs(organ_x - ex) + abs(organ_y - ey) == 2:
                        # Find the protein in between
                        mid_x = (organ_x + ex) // 2
                        mid_y = (organ_y + ey) // 2
                        
                        # Check if there's a protein at the midpoint
                        for px, py, _ in proteins:
                            if (px, py) == (mid_x, mid_y):
                                # Grow a tentacle on the protein facing the enemy
                                direction = get_harvester_direction(mid_x, mid_y, ex, ey)
                                return f"GROW {organ_id} {px} {py} TENTACLE {direction}"
        
        # Third priority: If no other space, grow on a protein
        # If there is no free space, grow on a protein
        # if not any(
        #     (organ_x + 1, organ_y) not in occupied_positions and
        #     (organ_x - 1, organ_y) not in occupied_positions and
        #     (organ_x, organ_y + 1) not in occupied_positions and
        #     (organ_x, organ_y - 1) not in occupied_positions
        #     for organ_x, organ_y, organ_id, _, _ in my_organs
        # ):
        #     # Grow on a protein if no other space
        #     for px, py, _ in proteins:
        #         if (px, py) not in occupied_positions:
        #             return f"GROW {organ_id} {px} {py} TENTACLE N"  # Replace with correct direction if needed

         # Second priority: Use SPORER if available and resources are sufficient
        if my_sporers and my_a >= 1 and my_b >= 1 and my_c >= 1 and my_d >= 1:
            sporer_x, sporer_y, sporer_id, sporer_dir = my_sporers[0]
            for px, py, _ in proteins:
                if not any(abs(org_x - px) + abs(org_y - py) == 1 for org_x, org_y, _, _, _ in my_organs):
                    spore_result = get_spore_position((px, py), occupied_positions, (sporer_x, sporer_y), width, height)
                    if spore_result:
                        spore_pos, needed_direction = spore_result
                        if sporer_dir == needed_direction and all(coord >= 0 for coord in spore_pos):
                            return f"SPORE {sporer_id} {spore_pos[0]} {spore_pos[1]}"
        
        # Third priority: Grow a SPORER if resources allow
        if not my_sporers and my_b >= 1 and my_d >= 1:
            best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
            if best_growth:
                organ_id, x, y, _, root_id = best_growth  # Include root_id
                if organ_id not in used_organs and root_id not in used_roots:
                    best_direction = get_best_sporer_direction(x, y, proteins)
                    used_organs.add(organ_id)
                    used_roots.add(root_id)  # Mark the ROOT as used
                    return f"GROW {organ_id} {x} {y} SPORER {best_direction}"
                
        # Fourth priority: Grow harvesters and expand
        best_growth = find_best_growth_position(my_organs, proteins, occupied_positions)
        if best_growth:
            organ_id, x, y, type_, direction = best_growth
            if x >= 0 and y >= 0 and x < width and y < height:
                if type_ == "BASIC" and my_a >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} BASIC"
                elif type_ == "HARVESTER" and my_c >= 1 and my_d >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif my_b >= 1 and my_d >= 1:
                    direction = get_best_sporer_direction(x, y, proteins)
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} SPORER {direction}"
                elif my_b >=1 and my_c >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} TENTACLE {direction}"
                elif my_c >= 1 and my_d >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif my_a >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} BASIC"
        expansion = find_best_expansion(my_organs, occupied_positions)
        if expansion:
            organ_id, x, y = expansion
            if x >= 0 and y >= 0 and x < width and y < height:
                if my_a >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} BASIC"
                if my_b >= 1 and my_c >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} TENTACLE N"
                if my_c >= 1 and my_d >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} HARVESTER N"
                if my_b >= 1 and my_d >= 1:
                    direction = get_best_sporer_direction(x, y, proteins)
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} SPORER {direction}"
                
        return "WAIT"



    # Reset used organs set at the start of each turn
    used_organs.clear()
    print_map(occupied_positions, width, height)

    for _ in range(required_actions_count):
        action = get_next_action()
        print(action)

