#!/usr/bin/env python
import random
from copy import copy


class Arrangement:
    def __init__(self, seats):
        self.seats = seats

    @staticmethod
    def default() -> "Arrangement":
        return Arrangement([
            [0,       0, 0, None],
            [None, None, 0],
            [None, None, 0],
            [None, None, 0]
        ])

    def __str__(self):
        out = ""
        for line in self.seats:
            for item in line:
                if item == 0:
                    out += "| | \t"
                elif item is None:
                    out += "-\t"
                else:
                    out += f"{item['id']}\t"

            out += "\n"

        return out

    def empty(self):
        for row in self.seats:
            for col in row:
                if col == 0:
                    continue

                col = None

    def get(self, i, j):
        return self.seats[i][j]

    def get_forbidden(self, i, j) -> list[int]:
        if i < 0 or j < 0 or i >= len(self.seats) or j >= len(self.seats[i]):
            return []

        if self.get(i, j) is None or self.get(i, j) == 0:
            return []

        return self.get(i, j)["cant_sit_with"]

    def has(self, user_id: int) -> bool:
        for row in self.seats:
            if user_id in row:
                return True

        return False

    def set(self, i, j, user):
        self.seats[i][j] = user

    def is_seat(self, i, j):
        return self.get(i, j) != 0

    def get_neighbors(self, i, j) -> list[int]:
        ns = []

        if j > 0 and self.get(i, j-1) is not None and self.get(i, j-1) != 0:
            ns.append(self.get(i, j-1)["id"])

        if j < len(self.seats[i])-1 and self.get(i, j+1) is not None and self.get(i, j+1) != 0:
            ns.append(self.get(i, j+1)["id"])

        return ns

    def can_seat(self, row, col, user):
        if self.get(row, col) is not None or not self.is_seat(row, col):
            return False

        if user["id"] in self.get_forbidden(row, col - 1):
            return False

        if user["id"] in self.get_forbidden(row, col + 1):
            return False

        nn = self.get_neighbors(row, col)

        for n in self.get_neighbors(row, col):
            if n in user["cant_sit_with"]:
                return False

        return True

    def seat_user(self, user):
        for i in range(0, len(self.seats)):
            for j in range(0, len(self.seats[i])):
                if self.can_seat(i, j, user):
                    return i, j

        return None, None

    @staticmethod
    def seat_users(arrangement: "Arrangement", users):
        bad_users = []

        for user in users:
            if arrangement.has(user["id"]):
                continue

            i, j = arrangement.seat_user(user)

            if i is None or j is None:
                bad_users.append(user)
            else:
                arrangement.set(i, j, user)

        return arrangement, bad_users


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

    seating_arrangement = Arrangement.default()

    solution, errors = seating_arrangement.seat_users(seating_arrangement, users)

    print(solution)
    print()
    print(errors)
