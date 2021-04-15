import properties
import views

RESOURCE_FUEL = 0
RESOURCE_GOLD = 1
RESOURCE_DIAMOND = 2

FIELD_SOIL = 0
FIELD_FUEL = 1
FIELD_GOLD = 2
FIELD_DIAMOND = 3
FIELD_LAVA = 4
FIELD_STONE = 5
FIELD_TUNNEL = 6

UNIT_WORKER = 0
UNIT_TRANSPORT = 1
UNIT_KAMIKAZE = 2
UNIT_GUARDIAN = 3


class Unit:
    def __init__(self, unit_type, position=(0, 0), player=None):
        self.type = unit_type
        self.position = position
        self.current_speed = properties.UNITS[self.type]["speed"]
        self.health = properties.UNITS[self.type]["max_health"]
        self.player = player
        self.view = views.UnitView(self)

    def is_can_move(self, new_position):
        return abs(new_position[0] - self.position[0]) + abs(
            new_position[1] - self.position[1]) == 1 and self.current_speed > 0

    def move(self, new_position, game_board):
        game_board.move_unit(self, new_position)

    def __str__(self):
        return str(self.type)


class Field:
    def __init__(self, field_type):
        self.units = list()
        self.type = field_type
        self.health = properties.FIELDS[self.type]["max_health"]
        self.view = views.FieldView(self)

    def is_busy(self):
        return len(self.units) >= properties.FIELDS[self.type]["max_units_count"]

    def add_unit(self, unit):
        if self.is_busy():
            raise Exception("Клетка занята")
        else:
            self.units.append(unit)

    def remove_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)
        else:
            raise Exception("Ошибка")

    def dig(self, current_player):
        damage = len([unit for unit in self.units if current_player.is_my_unit(unit)]) * \
                 properties.FIELDS[self.type]["resources_per_step"]
        self.health -= damage
        if self.health <= 0:
            self.dig_out()

    def refresh(self, current_player):
        if len(self.units) > 0:
            self.dig(current_player)

    def dig_out(self):
        if properties.FIELDS[self.type]["next_ground"] is None:
            import random
            new_type = random.choice(
                [f["type"] for f in properties.FIELDS if f["is_auto_generated"] and f["type"] != FIELD_DIAMOND])
        else:
            new_type = properties.FIELDS[self.type]["next_ground"]
        self.type = new_type

    def update(self, delta_time):
        # self.view.update(delta_time)
        pass

    @staticmethod
    def get_random():
        import random
        return Field(
            field_type=random.choice([prop["type"] for prop in properties.FIELDS if prop["is_auto_generated"]]))


class Board:
    def __init__(self, board_size=(0, 0)):
        self.size = board_size
        self.fields = [[Field(FIELD_SOIL)]]

    def get_field(self, position):
        return self.fields[position[1]][position[0]]

    def add_unit(self, unit, position):
        field = self.get_field(position)
        field.add_unit(unit)

    def remove_unit(self, unit):
        field = self.get_field(unit.position)
        field.remove_unit(unit)

    def move_unit(self, unit, new_position):
        if unit.is_can_move(new_position):
            new_field = self.get_field(new_position)
            old_field = self.get_field(unit.position)
            if not new_field.is_busy():
                old_field.remove_unit(unit)
                new_field.add_unit(unit)

    @staticmethod
    def get_random(board_size):
        board_board = Board(board_size=board_size)
        board_board.fields = [[Field.get_random() for x in range(board_size[0])] for y in range(board_size[1])]
        return board_board


class Player:
    def __init__(self, name, turn, game_board: Board, base_position=(0, 0)):
        self.name = name
        self.turn = turn
        self.board = game_board
        self.base_position = base_position
        self.resources = {
            res["type"]: res["start_count"] for res in properties.RESOURCES
        }
        self.units = []
        for unit_property in properties.UNITS:
            for i in range(unit_property["start_count"]):
                self.units.append(Unit(unit_property["type"], base_position, self))

    def __eq__(self, other):
        return self.name == other.name

    def is_my_unit(self, unit: Unit):
        return unit in self.units

    def move_unit(self, unit: Unit, new_position: tuple):
        if self.is_my_unit(unit):
            unit.move(new_position, self.board)

    def buy_unit(self, unit_type: int):
        cost = properties.UNITS[unit_type]["cost"]
        if self.resources[RESOURCE_GOLD] >= cost:
            if not self.board.get_field(self.base_position).is_busy():
                self.resources[RESOURCE_GOLD] -= cost
                self.board.add_unit(Unit(unit_type, self.base_position, self))

    def __str__(self):
        return self.resources.__str__() + '\n' + ' '.join([unit.__str__() for unit in self.units])


class Game:
    def __init__(self):
        self.board = Board.get_random((10, 10))

        self.board.fields[0][4].type = FIELD_TUNNEL
        self.board.fields[0][5].type = FIELD_TUNNEL

        self.board.fields[9][4].type = FIELD_TUNNEL
        self.board.fields[9][5].type = FIELD_TUNNEL

        self.players = [Player("nikita", 0, self.board, (0, 4)), Player("misharin", 1, self.board, (9, 5))]

        self.cur_player = self.players[0]

        for player in self.players:
            for unit in player.units:
                self.board.add_unit(unit, player.base_position)

    def next_turn(self):
        pass


if __name__ == '__main__':
    board = Board.get_random((10, 10))
    print(Player("Nikita", 0, board))
