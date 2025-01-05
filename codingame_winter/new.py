import sys
import math

width, height = [int(i) for i in input().split()]
harvesting_proteins = set()

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

import sys

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
                        if my_c >= 1 and my_d >= 1:
                            harvesting_proteins.add((px, py))
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

def is_in_front_of_tentacle(grow_x, grow_y, enemy_x, enemy_y, enemy_type, enemy_tentacles):
    """
    Determines if the given position (grow_x, grow_y) is in front of an enemy tentacle.
    """
    print(f"{grow_x} {grow_y}inside is_in_front_of_tentacle", file=sys.stderr)
    for tx, ty, t_dir in enemy_tentacles:
        if enemy_x == tx and enemy_y == ty:
            if t_dir == 'N' and grow_y - 1 == ty:
                return True
            if t_dir == 'S' and grow_y + 1 == ty:
                return True
            if t_dir == 'E' and grow_x - 1 == tx:
                return True
            if t_dir == 'W' and grow_x + 1 == tx:
                return True
    print(f"before false", file=sys.stderr)
    return False
            

def get_growth_direction(organ_x, organ_y, target_x, target_y):
    """
    Calculate the direction to grow towards a target position.
    The direction is returned as one of the following: 'N', 'S', 'E', 'W'.
    """
    if target_x == organ_x and target_y < organ_y:
        return 'N'  # North
    elif target_x == organ_x and target_y > organ_y:
        return 'S'  # South
    elif target_y == organ_y and target_x < organ_x:
        return 'W'  # West
    elif target_y == organ_y and target_x > organ_x:
        return 'E'  # East
    else:
        # If the target is not directly adjacent, return None (or handle as needed)
        return None

def grow_tentacle_or_harvester(organ_x, organ_y, organ_id, target_x, target_y, growth_type):
    """
    Grow a tentacle or harvester in the correct direction towards the target.
    """
    # Get the direction to grow towards the target
    direction = get_growth_direction(organ_x, organ_y, target_x, target_y)
    
    if direction:
        occupied_positions.add((target_x, target_y))
        return f"GROW {organ_id} {target_x} {target_y} {growth_type} {direction}"
    else:
        # Handle case where no valid direction can be calculated (if needed)
        return None



while True:
    enemy_tentacles = []
    proteins = []
    my_organs = []
    my_sporers = []
    enemy_organs = []
    enemy_positions = set()
    occupied_positions = set()
    wall_positions = set()
    spored = set()
    my_organ_positions = set()
    
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
            my_organ_positions.add((x, y))
            if type_ == "SPORER":
                my_sporers.append((x, y, organ_id, organ_dir))
        elif owner == 0:
            enemy_organs.append((x, y, type_))
            enemy_positions.add((x, y))
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
        elif owner == -1:
            if type_ == "WALL":
                wall_positions.add((x, y))


                
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
                        

        # Function to check if there are at least 6 consecutive free spaces in a direction
        def check_free_space_in_direction(start_x, start_y, direction):
            free_space_count = 0
            x, y = start_x, start_y
            
            while 0 <= x < width and 0 <= y < height:
                if (x, y) in wall_positions or (x, y) in enemy_occupied_positions or (x, y) in my_organ_positions:
                    break
                free_space_count += 1
                if free_space_count >= 6:
                    return True
                # Move to the next block in the given direction
                if direction == 'N':
                    y -= 1
                elif direction == 'S':
                    y += 1
                elif direction == 'E':
                    x += 1
                elif direction == 'W':
                    x -= 1
            
            return False
        
        # First priority: SPORER action (create ROOTs and expand)
        for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
            if organ_type == "SPORER" and my_b >= 1 and my_d >= 1:
                # Look for free spaces around the SPORER (North, South, East, West)
                directions = [
                    ('N', organ_x, organ_y - 1),
                    ('S', organ_x, organ_y + 1),
                    ('E', organ_x + 1, organ_y),
                    ('W', organ_x - 1, organ_y)
                ]
                
                # Try to spore a ROOT in the free direction if there are at least 6 consecutive free spaces
                for dir_, ax, ay in directions:
                    if check_free_space_in_direction(ax, ay, dir_):
                        # If there are at least 6 free spaces, grow the SPORER
                        occupied_positions.add((ax, ay))  # Mark the position as occupied
                        return f"SPORE {organ_id} {ax} {ay}"
        
        # Second priority: Expand from newly created ROOTs
        # Check if any ROOTs have been created and try to expand from them
    
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
                    
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, _, _ in my_organs:
                for ex, ey, enemy_type in enemy_organs:
                    # Check for proteins in between the organ and the enemy
                    if abs(organ_x - ex) + abs(organ_y - ey) == 2:
                        # Find the protein in between
                        mid_x = (organ_x + ex) // 2
                        mid_y = (organ_y + ey) // 2

                        # Check if there's a protein at the midpoint
                        for px, py, _ in proteins:
                            if (px, py) == (mid_x, mid_y):
                                # Check if the position is in front of an enemy tentacle
                                if is_in_front_of_tentacle(px, py, ex, ey, enemy_type, enemy_tentacles):
                                    continue  # Skip this case if the position is in front of a tentacle

                                # Grow a tentacle on the protein facing the enemy
                                print(f"is it here???", file=sys.stderr)
                                direction = get_harvester_direction(mid_x, mid_y, ex, ey)
                                return f"GROW {organ_id} {px} {py} TENTACLE {direction}"

        if my_c < 1 or my_d < 1:
            for organ_x, organ_y, organ_id, organ_type, organ_dir in my_organs:
                for px, py, _ in proteins:
                    # Skip if protein is already being harvested
                    if (px, py) in harvesting_proteins:
                        continue

                    # Check adjacency to the organ
                    if abs(organ_x - px) + abs(organ_y - py) == 1:
                        # Ensure position is safe from enemy tentacles
                        is_safe = all(
                            not is_in_front_of_tentacle(px, py, ex, ey, enemy_type, enemy_tentacles)
                            for ex, ey, enemy_type in enemy_organs
                        )
                        if is_safe:
                            # Determine growth type and direction
                            print("inside safe", file=sys.stderr)
                            if my_a >= 1:
                                growth_type = "BASIC"
                                direction = None  # No direction needed for BASIC
                            elif my_b >= 1 and my_d >= 1:
                                growth_type = "SPORER"
                                direction = get_best_sporer_direction(px, py, proteins)
                            elif my_b >= 1 and my_c >= 1:
                                growth_type = "TENTACLE"
                                direction = get_harvester_direction(organ_x, organ_y, px, py)

                            # Add position to occupied and return the growth command
                            occupied_positions.add((px, py))
                            if direction:
                                return f"GROW {organ_id} {px} {py} {growth_type} {direction}"
                            return f"GROW {organ_id} {px} {py} {growth_type}"
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
            for o_x, o_y, o_id, o_type, o_dir in my_organs:
                if o_id == organ_id:
                    organ_x, organ_y = o_x, o_y
                    break
            if x >= 0 and y >= 0 and x < width and y < height:
                if my_a >= 1:
                    occupied_positions.add((x, y))
                    return f"GROW {organ_id} {x} {y} BASIC"
                if my_b >= 1 and my_c >= 1:
                    # Assuming (x, y) is the target position for the tentacle
                    result = grow_tentacle_or_harvester(organ_x, organ_y, organ_id, x, y, "TENTACLE")
                    if result:
                        return result
                if my_c >= 1 and my_d >= 1:
                    # Assuming (x, y) is the target position for the harvester
                    result = grow_tentacle_or_harvester(organ_x, organ_y, organ_id, x, y, "HARVESTER")
                    if result:     ## *problem sending organ_x and organ_y)
                        return result
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

