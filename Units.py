from Map import Board


class UnitTypes:
    WORKER = 0
    TRANSPORT = 1
    KAMIKAZE = 2
    GUARDIAN = 3


class Unit:
    def __init__(self, unit_type=UnitTypes.WORKER, position=(0, 0)):
        self.type = unit_type
        self.position = position
        self.speed = 3
        self.health = 10

    def is_can_move(self, new_position):
        return abs(new_position[0] - self.position[0]) + abs(new_position[1] - self.position[1]) == 1

    def move(self, new_position, board):
        board.move_unit(self, new_position)
