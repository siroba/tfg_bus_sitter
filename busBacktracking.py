from utils import draw_bus, pasajeros_a_matriz, get_row_col


def existe_hermano_nivel_k(x, M, k):
    return x[k] < M - 1


def siguiente_hermano_nivel_k(x, k):
    x[k] = x[k] + 1

    return x, k


def valor(X, k):
    return sum(1 for i in range(1, k + 1) if X[i] != 0)


"""
# Entradas test
users = [
    {"id": 1, "cant_sit_with": [2, 3]},
    {"id": 2, "cant_sit_with": [1, 8, 4]},
    {"id": 3, "cant_sit_with": [2, 1]},
    {"id": 4, "cant_sit_with": [2, 8]},
    {"id": 5, "cant_sit_with": [2, 4, 6]},
    {"id": 6, "cant_sit_with": [2]},
    {"id": 7, "cant_sit_with": [2, 1, 4, 6]},
    {"id": 8, "cant_sit_with": [2]}
]

seats = [
    [None, 0, None, None, 0],
    [0, 0, None],
    [0, 0, None],
    [0, 0, None]
]

# Crear la matriz de distancias
P = len(users)  # Número de pasajeros
D = np.zeros((P + 1, P + 1), dtype=int)
for user in users:
    for other in user["cant_sit_with"]:
        D[user["id"], other] = 1
        D[other, user["id"]] = 1  # Asumimos que la relación es simétrica


# Crear la matriz de asientos
 R, C = len(seats), max(len(row) for row in seats)
 A = np.full((R + 1, C + 1), -1)  # Matriz de asientos (Se agrega una fila y columna extra para manejar índices desde 1)
pasillos = np.zeros((R + 1, C + 1), dtype=int)  # Matriz de pasillos
seat_num = 1
for i, row in enumerate(seats, start=1):
    for j, seat in enumerate(row, start=1):
        if seat is not None:
            A[i, j] = seat_num
            seat_num += 1
        else:
            pasillos[i, j] = 1
"""


def calcular_asientos_laterales(A, R, C, X_k):
    n_row, n_col = get_row_col(X_k, R, C)

    # Calcular los asientos laterales
    laterales = []
    if n_col - 1 > 0 and A[n_row][n_col - 1] == 0:  # Asiento a la izquierda
        laterales.append(A[n_row][n_col - 1])
    if n_col + 1 < C and A[n_row][n_col + 1] == 0:  # Asiento a la derecha
        laterales.append(A[n_row][n_col + 1])
    return laterales


def correcto(D, A, R, C, P, k, X):
    n_row, n_col = get_row_col(X[k], R, C)

    # Chequear si el asiento puede ser usado por algún pasajero
    if A[n_row][n_col] == -1:
        return False

    # Chequear si algún pasajero ya ha sido sentado en el asiento X[k]
    for i in range(k):
        if X[i] == X[k]:
            return False

    # Calcular una lista con los asientos laterales al asiento X[k]
    l = calcular_asientos_laterales(A, R, C, X[k])

    # Comprobar si el asiento X[k] del pasajero k es compatible con los asientos asignados a los pasajeros anteriores
    # 1 .. k-1
    for i in range(k-1):
        i_row, i_col = get_row_col(X[i], R, C)

        if X[i] == -1:
            continue

        if (abs(i_col - n_col) == 1) and i_row == n_row and D[i][k] == 1:
            return False

    # El asiento está libre y es compatible con los asientos asignados previamente
    return True


def Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k, X, X_mejor, v_mejor):
    X[k] = -1
    M = R * C  # Número total de asientos
    while existe_hermano_nivel_k(X, M, k):
        X, k = siguiente_hermano_nivel_k(X, k)
        if k == P and correcto(D, A, R, C, P, k, X):
            v_actual = valor(X, k)
            if v_actual > v_mejor[0]:
                v_mejor[0] = v_actual
                X_mejor = X[1:]
        elif k != P and correcto(D, A, R, C, P, k, X):
            D, A, R, C, P, k, X, X_mejor, v_mejor = Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k + 1, X, X_mejor, v_mejor)

    return D, A, R, C, P, k, X, X_mejor, v_mejor


def main():
    # Definir datos de entrada
    users = [
        {"id": 1, "cant_sit_with": [2, 3]},
        {"id": 2, "cant_sit_with": [1, 8, 4]},
        {"id": 7, "cant_sit_with": [2, 1]},
        {"id": 4, "cant_sit_with": [2, 8]},
        {"id": 5, "cant_sit_with": [2, 4, 6]},
        {"id": 6, "cant_sit_with": [2]},
        {"id": 3, "cant_sit_with": [2, 1, 4, 6]},
        {"id": 8, "cant_sit_with": [2]}
    ]
    D = pasajeros_a_matriz(users)

    A = [
        [-1, 0, -1, 0],
        [0, 0, -1, -1],
        [0, 0, -1, -1],
        [0, 0, -1, -1],
    ]
    # Datos de entrada definidos previamente, insertar aquí
    R, C = 4, 4
    P = 8  # Número total de pasajeros
    M = R * C  # Número total de asientos

    # Inicializar tuplas
    X = [-1 for _ in range(P + 1)]  # Solución actual (Se agrega una posición extra para manejar índices desde 1)
    X_mejor = [-1 ** P]  # Mejor solución encontrada (Se agrega una posición extra para manejar índices desde 1)
    v_mejor = [0]  # Mejor valor encontrado

    k = 1  # Nivel inicial del backtracking

    X[k] = -1  # preparar_recorrido_nivel_k(X, k)

    while existe_hermano_nivel_k(X, M, k):
        siguiente_hermano_nivel_k(X, k)
        if correcto(D, A, R, C, P, k, X):
            if k == P:
                v_actual = valor(X, k)
                if v_actual > v_mejor[0]:
                    v_mejor[0] = v_actual
                    X_mejor = X[1:]
            else:
                D, A, R, C, P, k, X, X_mejor, v_mejor = Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k + 1, X, X_mejor, v_mejor)

    print("Mejor solución encontrada:")
    print("Valor: ", v_mejor[0])
    print("Asignación de asientos: ", X_mejor)
    draw_bus(X_mejor, A)


if __name__ == '__main__':
    main()
