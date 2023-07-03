def get_adjacent(cords):
    adjacent_lst = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0) and (j == 0):
                continue

            adjacent_cord = (abs(cords[0] + i), abs(cords[1] + j))

            if (cords[0] + i) < 0 or (cords[1] + j) > 5 or adjacent_cord in adjacent_lst:
                continue

            adjacent_lst.append(adjacent_cord)

    return adjacent_lst


print(get_adjacent((3, 4)))