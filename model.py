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
        dist = abs(new_position[0] - self.position[0]) + abs(new_position[1] - self.position[1])
        return dist == 1 and self.current_speed > 0

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

    @staticmethod
    def get_random():
        import random
        return Field(
            field_type=random.choice([prop["type"] for prop in properties.FIELDS if prop["is_auto_generated"]]))


class Board:
    def __init__(self, board_size):
        self.size = board_size
        self.fields = [[Field.get_random() for x in range(board_size[0])] for y in range(board_size[1])]
        self.view = views.BoardView(self)

    def get_field(self, position):
        return self.fields[position[1]][position[0]]

    def add_unit(self, unit, position):
        field = self.get_field(position)
        if not field.is_busy():
            field.units.append(unit)
            self.view.add_unit_view(unit.view, field)

    def remove_unit(self, unit):
        field = self.get_field(unit.position)
        if unit in field.units:
            field.remove(unit)
            #self.view.add_unit_view(unit.view, field)

    def move_unit(self, unit, new_position):
        if unit.is_can_move(new_position):
            new_field = self.get_field(new_position)
            old_field = self.get_field(unit.position)
            if not new_field.is_busy():
                unit.position = new_position
                self.remove_unit(unit)
                self.add_unit(unit, new_position)

    def next_turn(self, cur_player):
        for y in range(len(self.fields)):
            for x in range(len(self.fields[y])):
                self.fields[y][x].dig(cur_player)


class Player:
    def __init__(self, name, turn, game_board: Board, base_position=(0, 0)):
        self.name = name
        self.turn = turn
        self.board = game_board
        self.base_position = base_position
        self.resources = {
            res["type"]: res["start_count"] for res in properties.RESOURCES
        }
        self.view = views.PlayerView(self)

    def __eq__(self, other):
        return self.turn == other.turn

    def is_my_unit(self, unit: Unit):
        return unit.player == self

    def move_unit(self, unit: Unit, new_position: tuple):
        if self.is_my_unit(unit):
            unit.move(new_position, self.board)

    def buy_unit(self, unit_type: int):
        cost = properties.UNITS[unit_type]["cost"]
        if self.resources[RESOURCE_GOLD] >= cost:
            if not self.board.get_field(self.base_position).is_busy():
                self.resources[RESOURCE_GOLD] -= cost
                unit = Unit(unit_type, self.base_position, self)
                self.board.add_unit(unit, self.base_position)


class Game:
    START_UNIT_COUNT = 3

    def __init__(self, player_count, board_size: tuple):
        self.player_count = player_count
        self.board_size = board_size
        self.board = Board(board_size)
        self.players = []
        self.cur_player_num = 0

        positions = self.get_players_position()
        for i in range(len(positions)):
            pos = positions[i]
            self.board.fields[pos[1]][pos[0]].type = FIELD_TUNNEL
            player = Player("Player" + str(i + 1), i, self.board, pos)
            self.players.append(player)
            for j in range(self.START_UNIT_COUNT):
                self.board.add_unit(Unit(UNIT_WORKER, pos, player), pos)

        self.view = views.GameView(self)

    def get_players_position(self):
        res = [
            (0, self.board_size[0] // 2),
            (self.board_size[0] - 1, self.board_size[1] // 2 + self.board_size[1] % 2),
            (self.board_size[0] // 2, 0),
            (self.board_size[0] // 2 + self.board_size[0] % 2, self.board_size[1] - 1)
        ]
        return res[:self.player_count]

    def get_unit(self, pos, index):
        field = self.get_field(pos)
        if field is not None:
            if index < len(self.board.get_field(pos).units):
                return self.board.get_field(pos).units[index]
        return None

    def get_field(self, pos):
        if 0 <= pos[0] <= self.board_size[0] and 0 <= pos[1] <= self.board_size[1]:
            return self.board.get_field(pos)
        return None

    def next_turn(self):
        self.cur_player_num = (self.cur_player_num + 1) % self.player_count
        self.board.next_turn(self.get_current_player())

    def get_current_player(self):
        return self.players[self.cur_player_num]

    def move_unit(self, unit, new_pos):
        if self.get_current_player().is_my_unit(unit):
            self.get_current_player().move_unit(unit, new_pos)

    def buy_unit(self, player, unit_type: int):
        if self.get_current_player() == player:
            self.get_current_player().buy_unit(unit_type)


if __name__ == '__main__':
    pass
