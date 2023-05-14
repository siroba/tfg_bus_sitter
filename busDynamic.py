#!/usr/bin/env python
import random
from copy import copy
import math

import numpy as np

class SeatAllocator:
    def __init__(self, users, seats):
        self.users = users
        self.seats = [seat for row in seats for seat in row]
        self.num_users = len(users)
        self.num_seats = len(self.seats)

    def solve(self):
        F = np.zeros((self.num_users + 1, self.num_seats + 1))
        decision = np.zeros((self.num_users + 1, self.num_seats + 1))

        for i in range(1, self.num_users + 1):
            for j in range(1, self.num_seats + 1):
                if self.seats[j - 1] is None or any(
                        (u is not None and u['id'] in self.users[i - 1]['cant_sit_with']) for u in self.seats[:j - 1]):
                    F[i][j] = F[i - 1][j]
                    decision[i][j] = 0
                else:
                    if F[i - 1][j] >= F[i - 1][j - 1] + 1:
                        F[i][j] = F[i - 1][j]
                        decision[i][j] = 0
                    else:
                        F[i][j] = F[i - 1][j - 1] + 1
                        decision[i][j] = 1
                        self.seats[j - 1] = self.users[i - 1]

        self.seats = [user if user is not None else {'id': None, 'cant_sit_with': []} for user in self.seats]

        placed_users = [user for user in self.seats if user['id'] is not None]
        unplaced_users = [user for user in self.users if user not in placed_users]

        return self.seats, unplaced_users, decision



if __name__ == '__main__':
    users = [
        {"id": 1, "cant_sit_with": [2, 3]},
        {"id": 2, "cant_sit_with": [1, 8, 4]},
        {"id": 3, "cant_sit_with": [2, 1]},
        {"id": 4, "cant_sit_with": [2, 8]},
        {"id": 5, "cant_sit_with": [2, 4,        6]},
        {"id": 6, "cant_sit_with": [2]},
        {"id": 7, "cant_sit_with": [2, 1, 4, 6]},
        {"id": 8, "cant_sit_with": [2]}
    ]

    seats = [[None, 0, None, None, 0], [0, 0, None], [0, 0, None], [0, 0, None]]

    sa = SeatAllocator(users, seats)
    solution, unplaced_users, decision = sa.solve()

    print("Placed users:")
    for i in range(len(solution)):
        if solution[i]['id'] is None:
            print("| |", end="\t")
        else:
            print(f"|{solution[i]['id']}|", end="\t")
        if (i+1) % 5 == 0:  # change to the number of seats in a row
            print()

    print("\nUnplaced users:")
    for user in unplaced_users:
        print(f"{user['id']}")

