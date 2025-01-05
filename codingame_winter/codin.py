# #wood 3
# # import sys
# # import math

# # # width: columns in the game grid
# # # height: rows in the game grid
# # width, height = [int(i) for i in input().split()]

# # # Keep track of last organ ID
# # last_organ_id = 1

# # # game loop
# # while True:
# #     # Track proteins and our organs
# #     proteins = []
# #     my_organs = []
# #     occupied_positions = set()  # Track all occupied positions
    
# #     entity_count = int(input())
# #     for i in range(entity_count):
# #         inputs = input().split()
# #         x = int(inputs[0])
# #         y = int(inputs[1])
# #         type_ = inputs[2]
# #         owner = int(inputs[3])
# #         organ_id = int(inputs[4])
# #         organ_dir = inputs[5]
        
# #         # Track occupied positions
# #         occupied_positions.add((x, y))
        
# #         # Track our organs
# #         if owner == 1:
# #             my_organs.append((x, y, organ_id))
# #             if organ_id > last_organ_id:
# #                 last_organ_id = organ_id
                
# #         # Track proteins
# #         if type_ in ['A', 'B', 'C', 'D']:
# #             proteins.append((x, y, type_))
# #     print(f"Proteins: {proteins}", file=sys.stderr)
# #     print(f"Occupied Positions: {occupied_positions}", file=sys.stderr)
# #     print(f"My Organs: {my_organs}", file=sys.stderr)
    
# #     my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
# #     opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
# #     required_actions_count = int(input())

# #     # Find nearest protein to our last organ
# #     if my_organs:
# #         last_x, last_y, _ = my_organs[-1]
        
# #         # Find closest unharvested protein
# #         nearest_protein = None
# #         min_dist = float('inf')
# #         for p_x, p_y, p_type in proteins:
# #             # Check if any of our organs are adjacent to this protein
# #             is_harvested = any(abs(org_x - p_x) + abs(org_y - p_y) == 1 
# #                              for org_x, org_y, _ in my_organs)
            
# #             if not is_harvested:
# #                 dist = abs(p_x - last_x) + abs(p_y - last_y)
# #                 if dist < min_dist:
# #                     min_dist = dist
# #                     nearest_protein = (p_x, p_y)
        
# #         if nearest_protein:
# #             px, py = nearest_protein
            
# #             # Calculate where we would grow
# #             new_x = last_x
# #             new_y = last_y
            
# #             if px > last_x:
# #                 new_x = last_x + 1
# #             elif px < last_x:
# #                 new_x = last_x - 1
# #             elif py > last_y:
# #                 new_y = last_y + 1
# #             elif py < last_y:
# #                 new_y = last_y - 1
            
# #             # Don't grow on proteins
# #             if (new_x, new_y) not in {(p[0], p[1]) for p in proteins}:
# #                 # If growing would put us next to protein, place harvester
# #                 if (abs(px - new_x) + abs(py - new_y)) == 1 and my_c >= 1 and my_d >= 1:
# #                     direction = 'N'  # Default
# #                     if px > new_x:
# #                         direction = 'E'
# #                     elif px < new_x:
# #                         direction = 'W'
# #                     elif py > new_y:
# #                         direction = 'S'
# #                     elif py < new_y:
# #                         direction = 'N'
                    
# #                     print(f"GROW {last_organ_id} {new_x} {new_y} HARVESTER {direction}")
# #                 else:
# #                     # Only grow if position is not occupied
# #                     if (new_x, new_y) not in occupied_positions:
# #                         print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
# #                     else:
# #                         print("WAIT")
# #             else:
# #                 # If would grow on protein, try growing in a different direction
# #                 possible_moves = [
# #                     (last_x + 1, last_y),
# #                     (last_x - 1, last_y),
# #                     (last_x, last_y + 1),
# #                     (last_x, last_y - 1)
# #                 ]
                
# #                 # Filter valid moves
# #                 valid_moves = [(x, y) for x, y in possible_moves 
# #                              if (x, y) not in occupied_positions 
# #                              and (x, y) not in {(p[0], p[1]) for p in proteins}]
                
# #                 if valid_moves:
# #                     new_x, new_y = valid_moves[0]  # Take first valid move
# #                     print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
# #                 else:
# #                     print("WAIT")
# #         else:
# #             # No unharvested proteins, grow in any valid direction
# #             possible_moves = [
# #                 (last_x + 1, last_y),
# #                 (last_x - 1, last_y),
# #                 (last_x, last_y + 1),
# #                 (last_x, last_y - 1)
# #             ]
            
# #             # Filter valid moves
# #             valid_moves = [(x, y) for x, y in possible_moves 
# #                          if (x, y) not in occupied_positions 
# #                          and (x, y) not in {(p[0], p[1]) for p in proteins}]
            
# #             if valid_moves:
# #                 new_x, new_y = valid_moves[0]  # Take first valid move
# #                 print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
# #             else:
# #                 print("WAIT")
# #     else:
# #         print("WAIT")


# # wood 2
# import sys
# import math

# # width: columns in the game grid
# # height: rows in the game grid
# width, height = [int(i) for i in input().split()]

# # Keep track of last organ ID
# last_organ_id = 1

# # game loop
# while True:
#     # Track proteins, organs and enemies
#     proteins = []
#     my_organs = []
#     enemy_organs = []
#     occupied_positions = set()
    
#     entity_count = int(input())
#     for i in range(entity_count):
#         inputs = input().split()
#         x = int(inputs[0])
#         y = int(inputs[1])
#         type_ = inputs[2]
#         owner = int(inputs[3])
#         organ_id = int(inputs[4])
#         organ_dir = inputs[5]
        
#         # Track occupied positions
#         occupied_positions.add((x, y))
        
#         # Track our organs
#         if owner == 1:
#             my_organs.append((x, y, organ_id))
#             if organ_id > last_organ_id:
#                 last_organ_id = organ_id
#         # Track enemy organs
#         elif owner == 0:
#             enemy_organs.append((x, y, type_))
                
#         # Track proteins
#         if type_ in ['A', 'B', 'C', 'D']:
#             proteins.append((x, y, type_))
#     print(f"Proteins: {proteins}", file=sys.stderr)
#     print(f"Occupied Positions: {occupied_positions}", file=sys.stderr)
#     print(f"My Organs: {my_organs}", file=sys.stderr)
    
#     my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
#     opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
#     required_actions_count = int(input())

#     if my_organs:
#         last_x, last_y, _ = my_organs[-1]
        
#         # First priority: Attack enemy if we're next to them and have resources
#         should_attack = False
#         attack_x, attack_y, attack_dir = None, None, None
        
#         for ex, ey, _ in enemy_organs:
#             # Check if we can place a tentacle next to enemy
#             possible_attack_positions = [
#                 (ex+1, ey, 'W'), (ex-1, ey, 'E'),
#                 (ex, ey+1, 'N'), (ex, ey-1, 'S')
#             ]
            
#             for ax, ay, dir_ in possible_attack_positions:
#                 # If we can reach this position from our last organ
#                 if abs(ax - last_x) + abs(ay - last_y) == 1:
#                     if (ax, ay) not in occupied_positions and my_b >= 1 and my_c >= 1:
#                         attack_x, attack_y = ax, ay
#                         attack_dir = dir_
#                         should_attack = True
#                         break
#             if should_attack:
#                 break
        
#         if should_attack:
#             print(f"GROW {last_organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}")
#             continue

#         # Second priority: Continue with protein harvesting strategy
#         nearest_protein = None
#         min_dist = float('inf')
#         for p_x, p_y, p_type in proteins:
#             is_harvested = any(abs(org_x - p_x) + abs(org_y - p_y) == 1 
#                              for org_x, org_y, _ in my_organs)
            
#             if not is_harvested:
#                 dist = abs(p_x - last_x) + abs(p_y - last_y)
#                 if dist < min_dist:
#                     min_dist = dist
#                     nearest_protein = (p_x, p_y)
        
#         if nearest_protein:
#             px, py = nearest_protein
#             new_x = last_x
#             new_y = last_y
            
#             if px > last_x:
#                 new_x = last_x + 1
#             elif px < last_x:
#                 new_x = last_x - 1
#             elif py > last_y:
#                 new_y = last_y + 1
#             elif py < last_y:
#                 new_y = last_y - 1
            
#             if (new_x, new_y) not in {(p[0], p[1]) for p in proteins}:
#                 if (abs(px - new_x) + abs(py - new_y)) == 1 and my_c >= 1 and my_d >= 1:
#                     direction = 'N'
#                     if px > new_x:
#                         direction = 'E'
#                     elif px < new_x:
#                         direction = 'W'
#                     elif py > new_y:
#                         direction = 'S'
#                     elif py < new_y:
#                         direction = 'N'
                    
#                     print(f"GROW {last_organ_id} {new_x} {new_y} HARVESTER {direction}")
#                 else:
#                     if (new_x, new_y) not in occupied_positions:
#                         print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
#                     else:
#                         print("WAIT")
#             else:
#                 possible_moves = [
#                     (last_x + 1, last_y),
#                     (last_x - 1, last_y),
#                     (last_x, last_y + 1),
#                     (last_x, last_y - 1)
#                 ]
                
#                 valid_moves = [(x, y) for x, y in possible_moves 
#                              if (x, y) not in occupied_positions 
#                              and (x, y) not in {(p[0], p[1]) for p in proteins}]
                
#                 if valid_moves:
#                     new_x, new_y = valid_moves[0]
#                     print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
#                 else:
#                     print("WAIT")
#         else:
#             possible_moves = [
#                 (last_x + 1, last_y),
#                 (last_x - 1, last_y),
#                 (last_x, last_y + 1),
#                 (last_x, last_y - 1)
#             ]
            
#             valid_moves = [(x, y) for x, y in possible_moves 
#                          if (x, y) not in occupied_positions 
#                          and (x, y) not in {(p[0], p[1]) for p in proteins}]
            
#             if valid_moves:
#                 new_x, new_y = valid_moves[0]
#                 print(f"GROW {last_organ_id} {new_x} {new_y} BASIC")
#             else:
#                 print("WAIT")
#     else:
#         print("WAIT")



###### SILVER LEAGUE - {349/559 Score - 9.88} 10:47PM 02/01/25 ######

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
    return None, None, None

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


def get_tentacle_targets(my_organs, enemy_organs, occupied_positions, enemy_occupied_positions):
    targets = []
    
    for organ_x, organ_y, organ_id, _, _ in my_organs:
        # Check enemies near organs
        for ex, ey, _ in enemy_organs:
            possible_attack_positions = [
                (ex + 1, ey, 'W'), (ex - 1, ey, 'E'),
                (ex, ey + 1, 'N'), (ex, ey - 1, 'S')
            ]
            
            for ax, ay, dir_ in possible_attack_positions:
                if (0 <= ax < width and 0 <= ay < height and 
                    abs(ax - organ_x) + abs(ay - organ_y) == 1 and
                    (ax, ay) not in occupied_positions and 
                    (ax, ay) not in enemy_occupied_positions):
                    targets.append((organ_id, ax, ay, dir_))
                    
        # Check proteins near enemy paths
        for px, py, _ in proteins:
            for ex, ey, _ in enemy_organs:
                if abs(px - ex) + abs(py - ey) <= 2:  # Enemy near protein
                    # Find position to defend protein
                    possible_positions = [
                        (px + 1, py, 'W'), (px - 1, py, 'E'),
                        (px, py + 1, 'N'), (px, py - 1, 'S')
                    ]
                    
                    for defend_x, defend_y, dir_ in possible_positions:
                        if (0 <= defend_x < width and 0 <= defend_y < height and
                            abs(defend_x - organ_x) + abs(defend_y - organ_y) == 1 and
                            (defend_x, defend_y) not in occupied_positions and
                            (defend_x, defend_y) not in enemy_occupied_positions):
                            targets.append((organ_id, defend_x, defend_y, dir_))
    
    return targets


def predict_enemy_tentacle_spots(my_organs, enemy_organs, occupied_positions):
    potential_threats = []
    
    # Check all possible enemy growth positions that could threaten our organs
    for ex, ey, _ in enemy_organs:
        for organ_x, organ_y, organ_id, _, _ in my_organs:
            # Calculate positions where enemy could grow a tentacle to attack us
            possible_enemy_positions = [
                (organ_x + 1, organ_y), (organ_x - 1, organ_y),
                (organ_x, organ_y + 1), (organ_x, organ_y - 1)
            ]
            
            for pos_x, pos_y in possible_enemy_positions:
                if (0 <= pos_x < width and 0 <= pos_y < height and
                    abs(pos_x - ex) + abs(pos_y - ey) == 1 and
                    (pos_x, pos_y) not in occupied_positions):
                    # Calculate direction for our tentacle
                    dx = organ_x - pos_x
                    dy = organ_y - pos_y
                    direction = ''
                    if abs(dx) > abs(dy):
                        direction = 'E' if dx < 0 else 'W'
                    else:
                        direction = 'S' if dy < 0 else 'N'
                    potential_threats.append((organ_id, pos_x, pos_y, direction))
    
    return potential_threats


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
                enemy_tentacles.append((x, y))  # Store the tentacle positions
                
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

    used_organs = set()  # Track organs used for growth in the current turn
    used_roots = set()  # Track which ROOTs have been used for growth

    def get_next_action():
        global used_organs, used_roots
        
        # Initialize enemy occupied positions
        enemy_occupied_positions = set()
        
        # Add positions of enemy organs and tentacles to the occupied positions
        for ex, ey, _ in enemy_organs:
            enemy_occupied_positions.add((ex, ey))
        for ex, ey in enemy_tentacles:  # Assuming you have a list for enemy tentacles
            enemy_occupied_positions.add((ex, ey))
        
        if not my_organs:
            return "WAIT"
        
        # First priority: Tentacle growth from any organ if an enemy is 1 block away
        should_attack = False
        attack_x, attack_y, attack_dir = None, None, None
        
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
                print(f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}")
                return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"
        
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
        global used_organs, used_roots
        
        enemy_occupied_positions = set()
        for ex, ey, _ in enemy_organs:
            enemy_occupied_positions.add((ex, ey))
        for ex, ey, organ_dir in enemy_tentacles:
            enemy_occupied_positions.add((ex, ey))
        
        if not my_organs:
            return "WAIT"
        
        # First priority: Block potential enemy tentacle spots
        if my_b >= 1 and my_c >= 1:
            threats = predict_enemy_tentacle_spots(my_organs, enemy_organs, occupied_positions)
            if threats:
                organ_id, x, y, direction = threats[0]
                occupied_positions.add((x, y))
                return f"GROW {organ_id} {x} {y} TENTACLE {direction}"
        
        # Second priority: Attack existing enemies
        if my_b >= 1 and my_c >= 1:
            targets = get_tentacle_targets(my_organs, enemy_organs, occupied_positions, enemy_occupied_positions)
            if targets:
                organ_id, x, y, direction = targets[0]
                occupied_positions.add((x, y))
                return f"GROW {organ_id} {x} {y} TENTACLE {direction}"
        
        # Second priority: Check if there's a protein between an organ and an enemy
        if my_b >= 1 and my_c >= 1:
            for organ_x, organ_y, organ_id, _, _ in my_organs:
                for ex, ey, _ in enemy_organs:
                    # Skip if the enemy organ is a tentacle (check against the list of enemy tentacles)
                    if (ex, ey) in [(tx, ty) for tx, ty, _ in enemy_tentacles]:
                        continue
                    
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
                    return f"GROW {organ_id} {x} {y} BASIC"
                elif type_ == "HARVESTER" and my_c >= 1 and my_d >= 1:
                    return f"GROW {organ_id} {x} {y} HARVESTER {direction}"
                elif not my_sporers and my_b >= 1 and my_d >= 1:
                    direction = get_best_sporer_direction(x, y, proteins)
                    return f"GROW {organ_id} {x} {y} SPORER {direction}"

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
