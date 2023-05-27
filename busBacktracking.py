import numpy as np


def preparar_recorrido_nivel_k(x, k):
    x[k] = -1


def existe_hermano_nivel_k(x, M, k):
    return x[k] < M


def siguiente_hermano_nivel_k(x, k):
    x[k] = x[k] + 1


def valor(X, P, k):
    return sum(1 for i in range(1, k + 1) if X[i] != 0)


def calcular_asientos_laterales(A, R, C, X_k):
    pos = X_k
    n_row = pos // (R + 1) + 1
    n_col = pos - (pos // (R + 1)) * C

    # Calcular los asientos laterales
    laterales = []
    if n_col - 1 > 0:  # Asiento a la izquierda
        laterales.append(A[n_row][n_col - 1])
    if n_col + 1 <= C:  # Asiento a la derecha
        laterales.append(A[n_row][n_col + 1])
    return laterales


def correcto(D, A, R, C, P, k, X):
    pos = X[k]
    n_row = pos // (R + 1) + 1
    n_col = pos - (pos // (R + 1)) * C

    # Chequear si el asiento puede ser usado por algún pasajero
    if A[n_row][n_col] == -1:
        return False

    # Chequear si algún pasajero ya ha sido sentado en el asiento X[k]
    for i in range(1, k):
        if X[i] == X[k]:
            return False

    # Calcular una lista con los asientos laterales al asiento X[k]
    l = calcular_asientos_laterales(A, R, C, X[k])

    # Chequear si el asiento X[k] del pasajero k es compatible con los asientos asignados a los pasajeros anteriores 1 .. k-1
    for i in range(1, k):
        if (X[i] in l) and (D[i][k] == 1):
            return False

    # El asiento esta libre y es compatible con los asientos asignados previamente
    return True


def Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k, X, X_mejor, v_mejor):
    X[k] = -1
    M = R * C  # Numero total de asientos
    while existe_hermano_nivel_k(X, M, k):
        siguiente_hermano_nivel_k(X, k)
        if k == P and correcto(D, A, R, C, P, k, X):
            v_actual = valor(X, P, k)
            if v_actual > v_mejor[0]:
                v_mejor[0] = v_actual
                X_mejor[:] = X[:]
        elif k != P and correcto(D, A, R, C, P, k, X):
            Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k + 1, X, X_mejor, v_mejor)

    def main():
        # Definir datos de entrada
        P = 4  # Numero de pasajeros
        R, C = 2, 3  # Numero de filas y columnas de asientos
        A = np.full((R + 1, C + 1),
                    0)  # Matriz de asientos (Se agrega una fila y columna extra para manejar indices desde 1)
        D = np.full((P + 1, P + 1),
                    0)  # Matriz de distancias entre pasajeros (Se agrega una fila y columna extra para manejar indices desde 1)

        # Inicializar tuplas
        X = [-1 for _ in range(P + 1)]  # Solución actual (Se agrega una posicion extra para manejar indices desde 1)
        X_mejor = [-1 for _ in range(
            P + 1)]  # Mejor solución encontrada (Se agrega una posicion extra para manejar indices desde 1)
        v_mejor = [0]  # Mejor valor encontrado

        k = 1  # Nivel inicial del backtracking

        preparar_recorrido_nivel_k(X, k)

        while existe_hermano_nivel_k(X, k, M):
            siguiente_hermano_nivel_k(X, k)
            if correcto(D, A, R, C, P, k, X):
                if k == P:
                    v_actual = valor(X, P, k)
                    if v_actual > v_mejor[0]:
                        v_mejor[0] = v_actual
                        X_mejor[:] = X[:]
                else:
                    Backtracking_AsignaAsientos_OPTIMA(D, A, R, C, P, k + 1, X, X_mejor, v_mejor)

        print("Mejor solución encontrada:")
        print("Valor: ", v_mejor[0])
        print("Asignación de asientos: ", X_mejor)

    if __name__ == '__main__':
        main()
