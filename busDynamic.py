#!/usr/bin/env python
import math
import random
from copy import copy


class SeatAllocator:
    def __init__(self, users, seats):
        self.users = users
        self.seats = seats
        self.num_users = len(users)
        self.num_seats = len(seats[0])
        self.table = [[math.inf for _ in range(self.num_seats)] for _ in range(self.num_users)]
        self.prev = [[None for _ in range(self.num_seats)] for _ in range(self.num_users)]

    def cost(self, i, j):
        if not self.seats[i][j]:
            return math.inf
        cost = 0
        for k in range(i):
            if self.seats[k][j] and self.users[k]['id'] in self.users[i]['cant_sit_with']:
                cost += 1
        return cost

    def solve(self):
        for j in range(self.num_seats):
            self.table[0][j] = self.cost(0, j)

        for i in range(1, self.num_users):
            for j in range(self.num_seats):
                c = self.cost(i, j)
                if c == math.inf:
                    self.table[i][j] = c
                    continue
                for k in range(self.num_seats):
                    if j == k:
                        continue
                    p = self.table[i-1][k] + c
                    if p < self.table[i][j]:
                        self.table[i][j] = p
                        self.prev[i][j] = k

        # backtrack to find solution
        j = self.table[self.num_users-1].index(min(self.table[self.num_users-1]))
        for i in range(self.num_users-1, -1, -1):
            if j is None:
                break
            self.seats[i][j] = self.users[i]
            j = self.prev[i][j]

        placed_users = [user for row in self.seats for user in row if user is not None]
        unplaced_users = [user for user in self.users if user not in placed_users]

        return self.seats, unplaced_users

if __name__ == '__main__':
    # Example usage:
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

    seats = [[None for _ in range(3)] for _ in range(8)]

    sa = SeatAllocator(users, seats)
    solution, unplaced_users = sa.solve()

    print("Placed users:")
    for row in solution:
        for user in row:
            if user is None:
                print("| |", end="\t")
            else:
                print(f"|{user['id']}|", end="\t")
        print()

# mirar los usuarios que no se han podido sentar
    print("\nUnplaced users:")
    for user in unplaced_users:
        print(f"{user['id']}")
