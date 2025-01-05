import sys
import math

width, height = [int(i) for i in input().split()]
harvesting_proteins = set()
my_a, my_b, my_c, my_d = 0, 0, 0, 0

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

def find_best_expansion(my_organs, occupied_positions, used_roots):
    """Find the best organ and position to expand to, avoiding walls and invalid coordinates."""
    for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
        if organ_root_id in used_roots:
            continue
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
            return organ_id, valid_positions[0][0], valid_positions[0][1], organ_root_id
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
    # for row in flipped_map:
        # sys.stderr.write(" ".join(row) + "\n")


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
                          for org_x, org_y, _, _, _, _ in my_organs)
        
        if not is_harvested:
            distance = abs(pos[0] - px) + abs(pos[1] - py)
            if distance < best_distance:
                best_distance = distance
                best_protein = (px, py, p_type)
    
    return best_protein, best_distance


def get_harvester_direction(x, y, px, py):
    """Determine harvester direction based on protein position."""
    if x == px:
        return 'S' if py > y else 'N'
    return 'E' if px > x else 'W'

def find_best_growth_position(my_organs, proteins, occupied_positions, used_roots):
    best_score = float('inf')
    best_growth = None

    for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
        if organ_root_id in used_roots:
            continue
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
                        best_growth = (organ_id, new_x, new_y, "HARVESTER", direction, organ_root_id)
                    else:
                        best_growth = (organ_id, new_x, new_y, "BASIC", None, organ_root_id)
            
        if (best_growth):
            orig, new_x, new_y, type_, direction, organ_root_id = best_growth
            if (new_x, new_y) in occupied_positions:
                continue

    return best_growth



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
    # print(f"{grow_x} {grow_y}inside is_in_front_of_tentacle", file=sys.stderr)
    for tx, ty, t_dir in enemy_tentacles:
        if enemy_x == tx and enemy_y == ty:
            if t_dir == 'N' and grow_y - 1 == ty:
                return True
            if t_dir == 'S' and grow_y + 1 == ty:
                return True
            if t_dir == 'E' and grow_x + 1 == tx:
                return True
            if t_dir == 'W' and grow_x - 1 == tx:
                return True
    # print(f"before false", file=sys.stderr)
    return False
            

def find_best_organ_to_grow_from(my_organs, non_prot_pos, width, height, used_roots,  min_free_blocks=6):
    """
    Find the best organ to grow from based on the most free blocks in a given direction.

    Parameters:
    - my_organs: A list of tuples containing (organ_x, organ_y, organ_id, organ_type, organ_dir) for each of your organs.
    - occupied_positions: A set of positions occupied by the organism.
    - enemy_occupied_positions: A set of positions occupied by enemy organisms or tentacles.
    - width: The width of the grid.
    - height: The height of the grid.
    - min_free_blocks: Minimum number of free blocks required in the direction.

    Returns:
    - (organ_id, new_x, new_y, direction): The best organ to grow from with its new position and direction.
    - None if no organ has enough free space in any direction.
    """
    
    best_organ = None
    max_free_count = 0
    best_direction = None
    best_new_x = None
    best_new_y = None

    # Iterate over each organ in your list
    for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
        # Initialize the best direction and max free space for this organ
        if organ_root_id in used_roots:
            continue
        max_direction_free_count = 0
        new_x, new_y = None, None

        # Check North (upward)
        free_count = 0
        for y in range(organ_y - 1, -1, -1):  # Move upwards in the y-axis
            if (organ_x, y) in non_prot_pos:
                break
            free_count += 1
        if free_count >= min_free_blocks and free_count > max_direction_free_count:
            best_direction = 'N'
            max_direction_free_count = free_count
            new_x, new_y = organ_x, organ_y - 1

        # Check South (downward)
        free_count = 0
        for y in range(organ_y + 1, height):  # Move downwards in the y-axis
            if (organ_x, y) in non_prot_pos:
                break
            free_count += 1
        if free_count >= min_free_blocks and free_count > max_direction_free_count:
            best_direction = 'S'
            max_direction_free_count = free_count
            new_x, new_y = organ_x, organ_y + 1

        # Check East (right)
        free_count = 0
        for x in range(organ_x + 1, width):  # Move right in the x-axis
            if (x, organ_y) in non_prot_pos:
                break
            free_count += 1
        if free_count >= min_free_blocks and free_count > max_direction_free_count:
            best_direction = 'E'
            max_direction_free_count = free_count
            new_x, new_y = organ_x + 1, organ_y

        # Check West (left)
        free_count = 0
        for x in range(organ_x - 1, -1, -1):  # Move left in the x-axis
            if (x, organ_y) in non_prot_pos:
                break
            free_count += 1
        if free_count >= min_free_blocks and free_count > max_direction_free_count:
            best_direction = 'W'
            max_direction_free_count = free_count
            new_x, new_y = organ_x - 1, organ_y

        # If this organ has the best direction with the most free space, update the best organ
        if best_direction and max_direction_free_count > max_free_count:
            best_organ = (organ_id, new_x, new_y, best_direction, organ_root_id)
            max_free_count = max_direction_free_count

    return best_organ  # Return the organ with the most free space in a direction, or None if no valid organ is found

def get_spore_position_in_direction(direction, sporer_pos, occupied_positions, width, height):
    sx, sy = sporer_pos

    # Generate positions based on the given direction
    if direction == 'N':
        positions = [(sx, y) for y in range(sy - 1, -1, -1)]
    elif direction == 'S':
        positions = [(sx, y) for y in range(sy + 1, height)]
    elif direction == 'E':
        positions = [(x, sy) for x in range(sx + 1, width)]
    elif direction == 'W':
        positions = [(x, sy) for x in range(sx - 1, -1, -1)]
    else:
        raise ValueError("Invalid direction. Use 'N', 'S', 'E', or 'W'.")

    # Find the position 1 block before the first occupied position or boundary
    for i, pos in enumerate(positions):
        if pos in occupied_positions:
            # Return the position before the occupied block
            return positions[i - 1] if i > 0 else None

    # If no occupied position is found, return the last position in the direction
    return positions[-1] if positions else None

def is_root_in_direction(position, direction, my_organs):
    """
    Checks if there is a ROOT organ in the specified row or column based on the given direction.

    Args:
        position (tuple): The (x, y) position to start checking from.
        direction (str): The direction to check ('N', 'S', 'E', 'W').
        my_organs (list): List of organs, each represented as a tuple
                          (organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id).

    Returns:
        bool: True if a ROOT organ is found in the specified row or column, False otherwise.
    """
    x, y = position

    # Filter out ROOT organs from my_organs
    root_organs = [(ox, oy) for ox, oy, _, organ_type, _, _ in my_organs if organ_type == "ROOT"]

    if direction == "N":
        # Check all ROOT organs in the same column but above the current position
        return any(ox == x and oy < y for ox, oy in root_organs)
    elif direction == "S":
        # Check all ROOT organs in the same column but below the current position
        return any(ox == x and oy > y for ox, oy in root_organs)
    elif direction == "E":
        # Check all ROOT organs in the same row but to the right of the current position
        return any(oy == y and ox > x for ox, oy in root_organs)
    elif direction == "W":
        # Check all ROOT organs in the same row but to the left of the current position
        return any(oy == y and ox < x for ox, oy in root_organs)

    return False  # If direction is invalid, return False

def detect_attacking_tentacle(enemy_tentacles, my_organs):
    for tx, ty, t_dir in enemy_tentacles:
        for ox, oy, _, _, _, _ in my_organs:
            # Check if the tentacle is adjacent to one of your organs
            if abs(tx - ox) + abs(ty - oy) == 1:
                return tx, ty, t_dir
    return None

# Predict the next target organ
def predict_next_target(attacking_tentacle, my_organs):
    tx, ty, t_dir = attacking_tentacle
    for ox, oy, _, _, _, _ in my_organs:
        # Check if the organ is in the tentacle's growth direction
        if t_dir == 'N' and ty > oy:
            return ox, oy
        elif t_dir == 'S' and ty < oy:
            return ox, oy
        elif t_dir == 'E' and tx < ox:
            return ox, oy
        elif t_dir == 'W' and tx > ox:
            return ox, oy
    return None

# Defensive growth logic
def grow_defensive_tentacle(attacking_tentacle, next_target, my_organs, occupied_positions):
    tx, ty, t_dir = attacking_tentacle
    ox, oy = next_target
    for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
        # Find a position to grow a tentacle between the tentacle and the target organ
        potential_positions = [
            (ox + 1, oy), (ox - 1, oy), (ox, oy + 1), (ox, oy - 1)
        ]
        for px, py in potential_positions:
            if (px, py) not in occupied_positions:
                # Determine the growth direction
                if px > organ_x:
                    grow_dir = 'E'
                elif px < organ_x:
                    grow_dir = 'W'
                elif py > organ_y:
                    grow_dir = 'S'
                elif py < organ_y:
                    grow_dir = 'N'
                
                # Grow the tentacle
                return f"GROW {organ_id} {px} {py} TENTACLE {grow_dir}"
    return None

def is_tentacle_next_to_coordinate(target_x, target_y, enemy_organs):

    # Define direction offsets
    direction_offsets = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0)
    }

    # Check all enemy organs
    for ex, ey, organ_dir in enemy_organs:
        if organ_dir in direction_offsets:
            dx, dy = direction_offsets[organ_dir]
            # Get the position the tentacle is facing
            facing_x, facing_y = ex + dx, ey + dy

            # Check if the tentacle is facing the target coordinate
            if facing_x == target_x and facing_y == target_y:
                return True

    return False

while True:
    enemy_tentacles = []
    proteins = []
    my_organs = []
    my_sporers = []
    enemy_organs = []
    occupied_positions = set()
    non_prot_pos = set()
    
    entity_count = int(input())
    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        type_ = inputs[2]  # WALL, ROOT, BASIC, TENTACLE, HARVESTER, SPORER, A, B, C, D
        owner = int(inputs[3])  # 1 if your organ, 0 if enemy organ, -1 if neither
        organ_id = int(inputs[4])  # id of this entity if it's an organ, 0 otherwise
        organ_dir = inputs[5]  # N,E,S,W or X if not an organ
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])
        
        occupied_positions.add((x, y))
        
        if owner == 1:
            my_organs.append((x, y, organ_id, type_, organ_dir, organ_root_id))
            non_prot_pos.add((x, y))
            if type_ == "SPORER":
                my_sporers.append((x, y, organ_id, organ_dir, organ_root_id))
        elif owner == 0:
            enemy_organs.append((x, y, type_))
            non_prot_pos.add((x, y))
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
                non_prot_pos.add((x, y))


                
        if type_ in ['A', 'B', 'C', 'D']:
            proteins.append((x, y, type_))
    
    sys.stderr.write("Occupied Positions Map:\n")
    
    # print(f"Proteins: {proteins}", file=sys.stderr)
    # print(f"My Organs: {my_organs}", file=sys.stderr)
    # print(f"My Sporers: {my_sporers}", file=sys.stderr)
    # print(f"enemy tentacles: {enemy_tentacles}", file=sys.stderr)
    
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())

    used_organs = set()  # Track organs used for growth in the current turn
    used_roots = set()  # Track which ROOTs have been used for growth

    def get_next_action():
        global used_organs, used_roots, my_a, my_b, my_c, my_d
        
        # Initialize enemy occupied positions
        enemy_occupied_positions = set()
        
        # Add positions of enemy organs and tentacles to the occupied positions
        for ex, ey, _ in enemy_organs:
            enemy_occupied_positions.add((ex, ey))
        for ex, ey, organ_dir in enemy_tentacles:  # Assuming you have a list for enemy tentacles
            enemy_occupied_positions.add((ex, ey))
        
        if not my_organs:
            return "WAIT"
                        


        # First priority: Tentacle growth from any organ if an enemy is 1 block away
        should_attack = False
        attack_x, attack_y, attack_dir = None, None, None
        
                    
        # if my_b >= 1 and my_c >= 1:
        #     # Loop through all organs to check if any organ is 1 block away from the enemy
        #     for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
        #         if organ_root_id in used_roots:
        #             continue
        #         for ex, ey, _ in enemy_organs:
        #             # Check if we can place a tentacle next to the enemy
        #             possible_attack_positions = [
        #                 (ex + 1, ey, 'W'), (ex - 1, ey, 'E'),
        #                 (ex, ey + 1, 'N'), (ex, ey - 1, 'S')
        #             ]
                    
        #             for ax, ay, dir_ in possible_attack_positions:
        #                 # If the organ is 1 block away from the enemy
        #                 if abs(ax - organ_x) + abs(ay - organ_y) == 1:
        #                     # Check if the position is not occupied by any of the enemy organs or tentacles
        #                     if (ax, ay) not in occupied_positions and (ax, ay) not in enemy_occupied_positions:
        #                         if my_b >= 1 and my_c >= 1:
        #                             attack_x, attack_y = ax, ay
        #                             attack_dir = dir_
        #                             should_attack = True
        #                             break
        #                 if should_attack:
        #                     break
        #             if is_tentacle_next_to_coordinate(attack_x, attack_y, enemy_tentacles):
        #                 continue
        #             if should_attack:
        #                 # Mark the position as occupied
        #                 used_roots.add(organ_root_id)
        #                 used_organs.add(organ_id)
        #                 occupied_positions.add((attack_x, attack_y))
        #                 my_b -= 1
        #                 my_c -= 1
        #                 print("this>", file=sys.stderr)
        #                 return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"
        
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
                for ex, ey, enemy_type in enemy_organs:
                    if organ_x - 1 == ex and organ_y - 1 == ey:
                        if (organ_x, organ_y - 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y - 1
                            attack_dir = 'W'
                            should_attack = True
                            break
                        elif (organ_x - 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x - 1, organ_y
                            attack_dir = 'N'
                            should_attack = True
                            break
                    if organ_x - 1 == ex and organ_y + 1 == ey:
                        if (organ_x, organ_y + 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y + 1
                            attack_dir = 'W'
                            should_attack = True
                            break
                        elif (organ_x - 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x - 1, organ_y
                            attack_dir = 'S'
                            should_attack = True
                            break
                    if organ_x + 1 == ex and organ_y - 1 == ey:
                        if (organ_x, organ_y - 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y - 1
                            attack_dir = 'E'
                            should_attack = True
                            break
                        elif (organ_x + 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x + 1, organ_y
                            attack_dir = 'N'
                            should_attack = True
                            break
                    if organ_x + 1 == ex and organ_y + 1 == ey:
                        if (organ_x, organ_y + 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y + 1
                            attack_dir = 'E'
                            should_attack = True
                            break
                        elif (organ_x + 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x + 1, organ_y
                            attack_dir = 'S'
                            should_attack = True
                            break
                if should_attack:
                    break
            if should_attack:
                # Mark the position as occupied
                occupied_positions.add((attack_x, attack_y))
                my_b -= 1
                my_c -= 1
                print("is it from here???part3", file=sys.stderr)
                used_organs.add(organ_id)
                used_roots.add(organ_root_id)
                return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"
                    
        
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
                for ex, ey, enemy_type in enemy_organs:
                    if organ_x == ex and organ_y + 1 == ey:
                        if (organ_x + 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x + 1, organ_y
                            attack_dir = 'S'
                            should_attack = True
                            break
                        elif (organ_x - 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x - 1, organ_y
                            attack_dir = 'S'
                            should_attack = True
                            break
                    if organ_x == ex and organ_y - 1 == ey:
                        if (organ_x + 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x + 1, organ_y
                            attack_dir = 'N'
                            should_attack = True
                            break
                        elif (organ_x - 1, organ_y) not in non_prot_pos:
                            attack_x, attack_y = organ_x - 1, organ_y
                            attack_dir = 'N'
                            should_attack = True
                            break
                    if organ_x + 1 == ex and organ_y == ey:
                        if (organ_x, organ_y + 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y + 1
                            attack_dir = 'E'
                            should_attack = True
                            break
                        elif (organ_x, organ_y - 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y - 1
                            attack_dir = 'E'
                            should_attack = True
                            break
                    if organ_x - 1 == ex and organ_y == ey:
                        if (organ_x, organ_y + 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y + 1
                            attack_dir = 'W'
                            should_attack = True
                            break
                        elif (organ_x, organ_y - 1) not in non_prot_pos:
                            attack_x, attack_y = organ_x, organ_y - 1
                            attack_dir = 'W'
                            should_attack = True
                            break
                if should_attack:
                    break
            if should_attack:
                # Mark the position as occupied
                occupied_positions.add((attack_x, attack_y))
                my_b -= 1
                my_c -= 1
                print("is it from here???", file=sys.stderr)
                used_organs.add(organ_id)
                used_roots.add(organ_root_id)
                return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"
            
        if my_b >= 1 and my_c >= 1:
            spaces = 3
            for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
                for ex, ey, enemy_type in enemy_organs:
                    if organ_x == ex and organ_y + spaces == ey:
                        if (organ_x , organ_y + 1) not in non_prot_pos and not is_tentacle_next_to_coordinate(organ_x, organ_y + 1, enemy_tentacles):
                            attack_x, attack_y = organ_x, organ_y + 1
                            attack_dir = 'S'
                            should_attack = True
                            break
                    if organ_x == ex and organ_y - spaces == ey:
                        if (organ_x, organ_y - 1) not in non_prot_pos and not is_tentacle_next_to_coordinate(organ_x, organ_y - 1, enemy_tentacles):
                            attack_x, attack_y = organ_x, organ_y - 1
                            attack_dir = 'N'
                            should_attack = True
                            break
                    if organ_x + spaces == ex and organ_y == ey:
                        if (organ_x + 1, organ_y) not in non_prot_pos and not is_tentacle_next_to_coordinate(organ_x + 1, organ_y, enemy_tentacles):
                            attack_x, attack_y = organ_x + 1, organ_y
                            attack_dir = 'E'
                            should_attack = True
                            break
                    if organ_x - spaces == ex and organ_y == ey:
                        if (organ_x - 1, organ_y) not in non_prot_pos and not is_tentacle_next_to_coordinate(organ_x - 1, organ_y, enemy_tentacles):
                            attack_x, attack_y = organ_x - 1, organ_y
                            attack_dir = 'W'
                            should_attack = True
                            break
                if should_attack:
                    break
            if should_attack:
                # Mark the position as occupied
                occupied_positions.add((attack_x, attack_y))
                my_b -= 1
                my_c -= 1
                print("is it from here part 2???", file=sys.stderr)
                used_organs.add(organ_id)
                used_roots.add(organ_root_id)
                return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"

        #spore
        if my_sporers and my_a >= 1 and my_b >= 1 and my_c >= 1 and my_d >= 1:
            for sporer_x, sporer_y, sporer_id, sporer_dir, organ_root_id in my_sporers:
                if sporer_id not in used_organs and organ_root_id not in used_roots:
                    # Check if the sporer has enough empty space in its facing direction
                    free_count = 0
                    if sporer_dir == 'N':  # Facing North
                        for y in range(sporer_y - 1, -1, -1):
                            if (sporer_x, y) in non_prot_pos:
                                break
                            free_count += 1
                    elif sporer_dir == 'S':  # Facing South
                        for y in range(sporer_y + 1, height):
                            if (sporer_x, y) in non_prot_pos:
                                break
                            free_count += 1
                    elif sporer_dir == 'E':  # Facing East
                        # print("in east?", file=sys.stderr)
                        for x in range(sporer_x + 1, width):
                            if (x, sporer_y) in non_prot_pos:
                                break
                            free_count += 1
                    elif sporer_dir == 'W':  # Facing West
                        for x in range(sporer_x - 1, -1, -1):
                            if (x, sporer_y) in non_prot_pos:
                                break
                            free_count += 1
                    # print(f"free_count: {free_count}", file=sys.stderr)
                    # Proceed only  if there is enough free space in the facing direction
                    
                    if free_count >= 4:
                        # for px, py, _ in proteins:
                        #     # Check if the protein is not already being harvested
                        #     is_harvested = any(
                        #         abs(org_x - px) + abs(org_y - py) == 1 for org_x, org_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs
                        #     )

                        #     if not is_harvested:
                        if not is_root_in_direction((sporer_x, sporer_y), sporer_dir, my_organs):
                            spore_result = get_spore_position_in_direction(
                                sporer_dir, (sporer_x, sporer_y), non_prot_pos, width, height
                            )
                            if spore_result:
                                spore_pos = spore_result
                                # Ensure the sporer is facing the needed direction
                                used_roots.add(organ_root_id)
                                used_organs.add(sporer_id)
                                my_a -= 1
                                my_b -= 1
                                my_c -= 1
                                my_d -= 1
                                return f"SPORE {sporer_id} {spore_pos[0]} {spore_pos[1]}"


        if not my_sporers and my_b >= 1 and my_d >= 1:
            best_growth = find_best_organ_to_grow_from(my_organs, non_prot_pos, width, height, used_roots)
            if best_growth:
                organ_id, x, y, best_direction, root_id = best_growth  # Include root_id
                # best_direction = get_best_sporer_direction(x, y, proteins)
                used_organs.add(organ_id)
                used_roots.add(root_id)  # Mark the ROOT as used
                my_b -= 1
                my_d -= 1
                return f"GROW {organ_id} {x} {y} SPORER {best_direction}"

        
        # # Second priority: Check if there's a protein between an organ and an enemy
        # if my_b >= 1 and my_c >= 1:
        #     for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
        #         for ex, ey, _ in enemy_organs:
        #             # Check for proteins in between the organ and the enemy
        #             if abs(organ_x - ex) + abs(organ_y - ey) == 2:
        #                 # Find the protein in between
        #                 mid_x = (organ_x + ex) // 2
        #                 mid_y = (organ_y + ey) // 2
                        
        #                 # Check if there's a protein at the midpoint
        #                 for px, py, _ in proteins:
        #                     if (px, py) == (mid_x, mid_y):
        #                         # Grow a tentacle on the protein facing the enemy
        #                         direction = get_harvester_direction(mid_x, mid_y, ex, ey)
        #                         occupied_positions.add((px, py))
        #                         used_roots.add(organ_root_id)
        #                         used_organs.add(organ_id)
        #                         my_b -= 1
        #                         my_c -= 1
        #                         return f"GROW {organ_id} {px} {py} TENTACLE {direction}"
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
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
                                if is_tentacle_next_to_coordinate(mid_x, mid_y, enemy_tentacles):
                                    continue  # Skip this case if the position is in front of a tentacle

                                # Grow a tentacle on the protein facing the enemy
                                direction = get_harvester_direction(px, py, ex, ey)
                                occupied_positions.add((px, py))
                                used_roots.add(organ_root_id)
                                used_organs.add(organ_id)
                                my_b -= 1
                                my_c -= 1
                                print("why would it come from here", file=sys.stderr)
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


        if my_c < 1 or my_d < 1:
            for organ_x, organ_y, organ_id, organ_type, organ_dir, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
                for px, py, _ in proteins:
                    # Skip if protein is already being harvested
                    if (px, py) in harvesting_proteins:
                        continue

                    # Check adjacency to the organ
                    if abs(organ_x - px) + abs(organ_y - py) == 1:
                        growth_type = None
                        direction = None
                        # Ensure position is safe from enemy tentacles
                        is_not_safe = is_tentacle_next_to_coordinate(px, py, enemy_tentacles)

                        if not is_not_safe:
                            # Determine growth type and direction
                            # print("inside safe", file=sys.stderr)
                            if my_a >= 1:
                                growth_type = "BASIC"
                                my_a -= 1
                                direction = None  # No direction needed for BASIC
                            elif my_b >= 1 and my_d >= 1:
                                growth_type = "SPORER"
                                my_b -= 1
                                my_d -= 1
                                direction = get_best_sporer_direction(px, py, proteins)
                            elif my_b >= 1 and my_c >= 1:
                                growth_type = "TENTACLE"
                                my_b -= 1
                                my_c -= 1
                                direction = get_harvester_direction(organ_x, organ_y, px, py)

                            # Add position to occupied and return the growth command
                            occupied_positions.add((px, py))
                            used_roots.add(organ_root_id)
                            used_organs.add(organ_id)
                            if not growth_type:
                                break
                            if direction:
                                print("no way it from here", file=sys.stderr)
                                return f"GROW {organ_id} {px} {py} {growth_type} {direction}"
                            return f"GROW {organ_id} {px} {py} {growth_type}"

        # Fourth priority: Grow harvesters and expand
        best_growth = find_best_growth_position(my_organs, proteins, occupied_positions, used_roots)
        if best_growth:
            cur_x = 2
            cur_y = 2
            organ_id, x, y, type_, direction, organ_root_id = best_growth
            for ox, oy, o_id, o_type, o_dir, o_root_id in my_organs:
                if organ_id == o_id:
                    cur_x = ox
                    cur_y = oy
                    break
            if x >= 0 and y >= 0 and x < width and y < height:
                if type_ == "BASIC" and my_a >= 1:
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    my_a -= 1
                    return f"GROW {organ_id} {x} {y} BASIC"
                elif type_ == "HARVESTER" and my_c >= 1 and my_d >= 1:
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    my_c -= 1
                    my_d -= 1
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif my_b >= 1 and my_d >= 1:
                    direction = get_best_sporer_direction(x, y, proteins)
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    if not direction:
                        direction = get_harvester_direction(cur_x, cur_y, x, y)
                    my_b -= 1
                    my_d -= 1
                    return f"GROW {organ_id} {x} {y} SPORER {direction}"
                elif my_b >=1 and my_c >= 1:
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    if not direction:
                        direction = get_harvester_direction(cur_x, cur_y, x, y)
                    my_b -= 1
                    my_c -= 1
                    print(f"inside tentacle - {x}, {y}", file=sys.stderr)
                    return f"GROW {organ_id} {x} {y} TENTACLE {direction}"
                elif my_c >= 1 and my_d >= 1:
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    if not direction:
                        direction = get_harvester_direction(cur_x, cur_y, x, y)
                    my_c -= 1
                    my_d -= 1
                    print(f"inside harvester", file=sys.stderr)
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif my_a >= 1:
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((x, y))
                    my_a -= 1
                    return f"GROW {organ_id} {x} {y} BASIC"
        expansion = find_best_expansion(my_organs, occupied_positions, used_roots)
        if expansion:
            cur_x = -2
            cur_y = -2
            organ_id, x, y, organ_root_id = expansion
            for ox, oy, o_id, o_type, o_dir, o_root_id in my_organs:
                if organ_id == o_id:
                    cur_x = ox
                    cur_y = oy
                    break
            if x >= 0 and y >= 0 and x < width and y < height:
                if my_a >= 1:
                    occupied_positions.add((x, y))
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    my_a -= 1
                    return f"GROW {organ_id} {x} {y} BASIC"
                if my_b >= 1 and my_c >= 1:
                    occupied_positions.add((x, y))
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    my_b -= 1
                    my_c -= 1
                    direction = get_harvester_direction(cur_x, cur_y, x, y)
                    return f"GROW {organ_id} {x} {y} TENTACLE {direction}"
                if my_c >= 1 and my_d >= 1:
                    occupied_positions.add((x, y))
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    my_c -= 1
                    my_d -= 1
                    direction = get_harvester_direction(cur_x, cur_y, x, y)
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                if my_b >= 1 and my_d >= 1:
                    direction = get_best_sporer_direction(x, y, proteins)
                    occupied_positions.add((x, y))
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    my_b -= 1
                    my_d -= 1
                    return f"GROW {organ_id} {x} {y} SPORER {direction}"
                

        return "WAIT"



    # Reset used organs set at the start of each turn
    used_organs.clear()
    # print_map(occupied_positions, width, height)

    for _ in range(required_actions_count):
        final_action = get_next_action()
        print(final_action)

