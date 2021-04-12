import random


def get_field_types():
    return [FieldTypes.__dict__[key] for key in list(FieldTypes.__dict__.keys()) if key.isupper()]


class Board:
    def __init__(self, board_size=(0, 0)):
        self.size = board_size
        self.fields = [[Field()]]

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
        board = Board(board_size=board_size)
        board.fields = [[Field.get_random() for x in range(board_size[0])] for y in range(board_size[1])]
        return board

    def __str__(self):
        lines = []
        for line in self.fields:
            res = []
            for field in line:
                res.append(str(field))

            lines.append(' '.join(res))
        return '\n'.join(lines)


class ResourceTypes:
    GOLD = 0
    OIL = 1
    DIAMOND = 2


class FieldTypes:
    SOIL = 0
    OIL = 1
    DIAMOND = 2
    GOLD = 3
    STONE = 4
    WATER = 5
    TUNNEL = 6


class Field:
    MAX_UNIT_COUNT = 3

    def __init__(self, field_type=FieldTypes.SOIL):
        self.type = field_type
        self.__units = list()
        self.property = FieldsProperties[self.type]
        self.health = self.property.max_health

    def is_busy(self):
        return len(self.__units) > self.property[self.type]

    def add_unit(self, unit):
        if self.is_busy():
            raise Exception("Клетка занята")
        else:
            self.__units.append(unit)

    def remove_unit(self, unit):
        if unit in self.__units:
            self.__units.remove(unit)
        else:
            raise Exception("Ошибка")

    def dig(self):
        damage = sum([unit.dig_power for unit in self.__units])
        self.health -= damage
        if self.health <= 0:
            self.dig_out()

    def dig_out(self):
        if FieldTypes.TUNNEL == self.type:
            self.type = random.choice(list(set(get_field_types()) - {FieldTypes.TUNNEL}))
        elif FieldTypes.WATER == self.type:
            self.type = FieldTypes.SOIL
        else:
            self.type = FieldTypes.TUNNEL

    @staticmethod
    def get_random():
        return Field(field_type=random.choice(get_field_types()))

    def __str__(self):
        return str(self.type)


class FieldProperty:
    def __init__(self, field_type, max_health, health_per_step, max_unit_count, resource_type=None,
                 resources_per_step=0, auto_generate=True):
        self.type = field_type
        self.max_health = max_health
        self.health_per_step = health_per_step
        self.resources_per_step = resources_per_step
        self.max_units_count = max_unit_count
        self.resources_type = resource_type
        self.auto_generate = auto_generate

    def __str__(self):
        return self.__dict__.__str__()


FieldsProperties = {
    FieldTypes.SOIL: FieldProperty(FieldTypes.SOIL, 10, 10, Field.MAX_UNIT_COUNT),
    FieldTypes.STONE: FieldProperty(FieldTypes.STONE, 30, 10, Field.MAX_UNIT_COUNT),
    FieldTypes.WATER: FieldProperty(FieldTypes.SOIL, 1, 10, Field.MAX_UNIT_COUNT),
    FieldTypes.OIL: FieldProperty(FieldTypes.OIL, 100, 10, Field.MAX_UNIT_COUNT,
                                  resource_type=ResourceTypes.OIL, resources_per_step=10),
    FieldTypes.GOLD: FieldProperty(FieldTypes.GOLD, 100, 10, Field.MAX_UNIT_COUNT,
                                   resource_type=ResourceTypes.GOLD, resources_per_step=10),
    FieldTypes.DIAMOND: FieldProperty(FieldTypes.DIAMOND, 100, 10, Field.MAX_UNIT_COUNT,
                                      resource_type=ResourceTypes.DIAMOND,
                                      resources_per_step=10),
    FieldTypes.TUNNEL: FieldProperty(FieldTypes.TUNNEL, 100, 10, Field.MAX_UNIT_COUNT)
}
