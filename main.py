import pygame
import random


class Board:
    def __init__(self, board_size=(0, 0)):
        self.size = board_size
        self._fields = [[]]

    @staticmethod
    def get_random(board_size):
        board = Board(board_size=board_size)
        board._fields = [[Field.get_random() for x in range(board_size[0])] for y in range(board_size[1])]
        return board


class FieldTypes:
    SOIL = 0
    OIL = 1
    DIAMOND = 2
    GOLD = 3
    STONE = 4
    WATER = 5
    TUNNEL = 6


class ResourceTypes:
    GOLD = 0
    OIL = 1
    DIAMOND = 2


class FieldProperty:
    def __init__(self, field_type, max_health, health_per_step, max_unit_count, resource_type=None,
                 resources_per_step=0):
        self.type = field_type
        self.max_health = max_health
        self.health_per_step = health_per_step
        self.resources_per_step = resources_per_step
        self.max_units_count = max_unit_count
        self.resources_type = resource_type

    def __str__(self):
        return self.__dict__.__str__()


class FieldsProperties:
    def __init__(self):
        self.__properties = dict()

        self.__properties[FieldTypes.SOIL] = FieldProperty(FieldTypes.SOIL, 10, 10, Field.MAX_UNIT_COUNT)
        self.__properties[FieldTypes.STONE] = FieldProperty(FieldTypes.STONE, 30, 10, Field.MAX_UNIT_COUNT)
        self.__properties[FieldTypes.WATER] = FieldProperty(FieldTypes.SOIL, 1, 10, Field.MAX_UNIT_COUNT)

        self.__properties[FieldTypes.OIL] = \
            FieldProperty(FieldTypes.OIL, 100, 10,
                          Field.MAX_UNIT_COUNT, resource_type=ResourceTypes.OIL,
                          resources_per_step=10)
        self.__properties[FieldTypes.GOLD] = \
            FieldProperty(FieldTypes.GOLD, 100, 10,
                          Field.MAX_UNIT_COUNT, resource_type=ResourceTypes.GOLD,
                          resources_per_step=10)
        self.__properties[FieldTypes.DIAMOND] = \
            FieldProperty(FieldTypes.DIAMOND, 100, 10,
                          Field.MAX_UNIT_COUNT, resource_type=ResourceTypes.DIAMOND,
                          resources_per_step=10)

    def __getitem__(self, item):
        return self.__properties[item]


class Field:
    MAX_UNIT_COUNT = 3

    def __init__(self, field_type=FieldTypes.SOIL):
        self.type = field_type
        self.__units = list()
        self.property = FieldsProperties[self.type]
        self.health = self.property.max_health

    def is_busy(self):
        return len(self.__units) > self.MAX_UNIT_COUNT

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
        pass

    def dig_out(self):
        if FieldTypes.TUNNEL == self.type:
            self.type = Field.get_random()
        else:
            self.type = FieldTypes.TUNNEL

    @staticmethod
    def get_random():
        return Field(field_type=random.randint(0, 6))


if __name__ == '__main__':
    field = Field.get_random()
    print(field)
    # pygame.init()
    # size = width, height = 800, 400
    # screen = pygame.display.set_mode(size)
    #
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     pygame.display.flip()
    # pygame.quit()
