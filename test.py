from Board import Board


b = Board()

loop = b.get_inner_loop_testing()
loop_cords = [i.get_cords() for i in loop]
print(loop_cords)

# already_done = []
# for i in loop:
#     print(i.get_cords(), i.get_colour())


# print(len(already_done))
# print(len(loop_cords))

for row in b.get_board_state():
    for i in row:
        print(i.get_cords(), i.get_colour())

