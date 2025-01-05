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





        if my_b >= 1 and my_c >= 1:
            # Loop through all organs to check if any organ is 1 block away from the enemy
            for organ_x, organ_y, organ_id, _, _, organ_root_id in my_organs:
                if organ_root_id in used_roots:
                    continue
                for ex, ey, _ in enemy_organs:
                    # If the organ is 1 block away from the enemy
                    if abs(ex - organ_x) + abs(ey - organ_y) == 2:
                        
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
                    used_roots.add(organ_root_id)
                    used_organs.add(organ_id)
                    occupied_positions.add((attack_x, attack_y))
                    return f"GROW {organ_id} {attack_x} {attack_y} TENTACLE {attack_dir}"