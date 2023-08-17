# x is a 6x6 matrix where each row is the number 2
x = [[2 for i in range(6)] for j in range(6)]

for i in x:
    print(i)

x = [x[i:i+6] for i in range(0, len(x), 6)]

for i in x:
    print(i)