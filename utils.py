def draw_bus(X, A):
    for i, col in enumerate(A):
        for j, item in enumerate(col):
            if item == -1:
                print(" X ", end="")
            else:
                found = -1
                for k, x_k in enumerate(X):
                    seat_n = i*len(col)+j
                    if x_k == seat_n:
                        found = k
                        break

                if found == -1:
                    print("(-)", end="")
                else:
                    print(f"({found+1})", end="")

        print()


"""
D = [
    #1  2  3  4  5  6  7  8
    [1, 0, 0, 1, 1, 1, 0, 1],  # 1
    [0, 1, 0, 0, 0, 0, 0, 0],  # 2
    [0, 0, 1, 1, 1, 1, 1, 1],  # 3
    [1, 0, 1, 1, 0, 1, 0, 0],  # 4
    [1, 0, 1, 0, 1, 0, 1, 1],  # 5
    [1, 0, 1, 1, 0, 1, 0, 1],  # 6
    [0, 0, 1, 0, 1, 0, 1, 1],  # 7
    [1, 0, 1, 0, 1, 1, 1, 1],  # 8
]
"""


def pasajeros_a_matriz(pasajeros):
    D = [[1 for _ in pasajeros] for _ in pasajeros]

    for pasajero in pasajeros:
        p_id = pasajero["id"]

        for other in pasajero["cant_sit_with"]:
            D[p_id-1][other-1] = 0
            D[other-1][p_id-1] = 0

    return D


def get_row_col(pos, R, C) -> tuple[int, int]:
    n_row = pos // R
    n_col = pos - (pos // R) * C

    return n_row, n_col
