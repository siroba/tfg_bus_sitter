class Bus:
    def __init__(self, seats):
        self.seats = seats

    def __getitem__(self, item) -> list[int]:
        return self.seats[item]

    def __len__(self):
        return len(self.seats)

    def __str__(self):
        out = ""
        for line in self.seats:
            for item in line:
                if item == 0:
                    out += "   \t"
                elif item is None:
                    out += "-\t"
                else:
                    out += f"{item}\t"

            out += "\n"

        return out

    @staticmethod
    def default() -> "Bus":
        return Bus([
            [None, None, 0, None, None],
            [None, None, 0, None, None],
            [None, None, 0, None, None]
        ])

    def set(self, i, j, v):
        self.seats[i][j] = v


def is_valid_seat(bus, user, row, col):
    cant_sit_with = user["cant_sit_with"]
    left_seat = bus[row][col - 1] if col > 0 else None
    right_seat = bus[row][col + 1] if col < len(bus[row]) - 1 else None

    if (left_seat not in cant_sit_with) and (right_seat not in cant_sit_with):
        return True
    return False


def dfs(bus, users, idx, memo):
    if idx == len(users):
        return bus, []

    if (str(bus), idx) in memo:
        return memo[(str(bus), idx)]

    best_bus = None
    best_remaining_users = users[idx:]

    user = users[idx]
    for i in range(len(bus)):
        for j in range(len(bus[i])):
            if bus[i][j] is None and is_valid_seat(bus, user, i, j):
                new_bus = Bus([row.copy() for row in bus.seats])
                new_bus.set(i, j, user["id"])
                result_bus, result_remaining_users = dfs(new_bus, users, idx + 1, memo)
                if len(result_remaining_users) < len(best_remaining_users):
                    best_bus = result_bus
                    best_remaining_users = result_remaining_users

    if best_bus is None:
        best_remaining_users = [user] + best_remaining_users

    memo[(str(bus), idx)] = (best_bus, best_remaining_users)
    return best_bus, best_remaining_users


def assign_seats(bus, users):
    result_bus, remaining_users = dfs(bus, users, 0, {})
    return result_bus, remaining_users

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

bus = Bus([
    [0,       0, 0, None],
    [None, None, 0, 0],
    [None, None, 0, 0],
    [None, None, 0, 0]
])
result_bus, remaining_users = assign_seats(bus, users)
print(result_bus)
print("Remaining users:", remaining_users)
