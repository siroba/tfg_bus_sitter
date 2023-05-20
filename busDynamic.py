#!/usr/bin/env python

import numpy as np


class SeatAllocator:
    def __init__(self, users, seats):
        self.users = users
        self.seats = [seat for row in seats for seat in row]
        self.num_users = len(users)
        self.num_seats = len(self.seats)

    def can_sit(self, user: int, seat: int) -> bool:
        """
        It checks the adjacent seats for blacklisted users
        :param user:
        :param seat:
        :return: true if the given user can seat at the given seat
        """
        blacklist = self.users[user]['cant_sit_with']

        if seat > 0 and self.seats[seat-1] in blacklist:
            return False

        if seat < self.num_seats-1 and self.seats[seat+1] in blacklist:
            return False

        return True


    def solve(self):
        F = np.full(
            (self.num_users + 1, self.num_seats + 1),
            -np.inf
        )
        decision = np.zeros((self.num_users + 1, self.num_seats + 1))

        # Casos base
        F[0, :] = 0  # No hay usuarios para asignar
        F[:, 0] = 0  # No hay asientos disponibles

        for i in range(1, self.num_users + 1):
            if self.users[i-1]['id'] in self.seats:
                continue

            for j in range(1, self.num_seats + 1):
                #
                if self.seats[j - 1] is None or not self.can_sit(i-1, j-1) or F[i - 1][j] >= F[i - 1][j - 1] + 1:
                    F[i][j] = F[i - 1][j]
                    decision[i][j] = 0
                else:
                    F[i][j] = max(F[i-1][j], F[i - 1][j - 1] + 1)
                    decision[i][j] = 1
                    self.seats[j - 1] = self.users[i - 1]

        # self.seats = [user if user is not None else {'id': None, 'cant_sit_with': []} for user in self.seats]
        # placed_users = [user for user in self.seats if user['id'] is not None]
        unplaced_users = [user for user in self.users if user not in [seat for seat in self.seats if seat is not None]]

        return decision, unplaced_users, decision


def reshape_to_variable_rows(flat_array, original_2d_array):
    # get lengths of each row in the original 2d array
    row_lengths = [len(row) for row in original_2d_array]

    new_2d_array = []
    i = 0  # start index for slicing flat_array
    for length in row_lengths:
        new_row = flat_array[i:i+length]
        new_2d_array.append(new_row)
        i += length  # move the start index to the end of the current slice

    return new_2d_array


def main():
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

    sa = SeatAllocator(users, seats)
    solution, unplaced_users, decision = sa.solve()
    trip_num = 1
    while unplaced_users:
        print(f"Trip number: {trip_num}")
        placed_users = []
        print("Placed users:")
        for user in solution:
            if user is not None:
                placed_users.append(user)
                print(f"User {user['id']}")

        print("Unplaced users:")
        for user in unplaced_users:
            print(f"User {user['id']}")

        print("Final seating arrangement:")

        for row in reshape_to_variable_rows(solution, seats):
            for seat in row:
                if seat is None:
                    print(" ", end="\t")
                else:
                    print(f"|{seat['id']}|", end="\t")
            print()

        print()

        seats = [[None, 0, None, None, 0], [0, 0, None], [0, 0, None], [0, 0, None]]
        sa = SeatAllocator(unplaced_users, seats)
        solution, unplaced_users, decision = sa.solve()
        trip_num += 1

    print("Decision matrix:")

    for i in range(len(decision)):
        for j in range(len(decision[i])):
            print(int(decision[i][j]), end=' ')
        print()

    print("Final seating arrangement:")

    for row in reshape_to_variable_rows(solution, seats):
        for seat in row:
            if seat is None:
                print(" ", end="\t")
            else:
                print(f"|{seat['id']}|", end="\t")
        print()

    print("\nAll users placed.")


if __name__ == '__main__':
    main()
