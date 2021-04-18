import pygame_gui
import pygame
from model import Field, Unit
import properties
import graphics


class Label(pygame_gui.elements.UILabel):
    HEIGHT = 24
    FONT_SIZE = 3.0

    def __init__(self, parent, rect, text="", width=0):
        super().__init__(
            relative_rect=rect,
            manager=parent.manager,
            parent_element=parent,
            text=f"""{text}""",
            anchors={
                "left": "left",
                "right": "left",
                "top": "top",
                "bottom": "bottom"
            })
        # self.text_colour = pygame.color.Color(255, 0 , 0)
        # self.bg_colour = pygame.color.Color(255, 0 , 0)

    def update(self, delta_time):
        super().update(delta_time)

    def set_text_color(self, color):
        self.text_colour = color


class Button(pygame_gui.elements.UIButton):
    HEIGHT = 30

    def __init__(self, parent, rect, text=""):
        super().__init__(
            relative_rect=rect,
            text=text,
            manager=parent.manager,
            anchors={
                "left": "left",
                "right": "left",
                "top": "top",
                "bottom": "bottom"
            }
        )


class InfoPanel(pygame_gui.elements.UIPanel):
    PADDING = 10
    WIDTH = 250

    def __init__(self, manager, position, labels_count):
        self.manager = manager
        self.labels_count = labels_count
        rect = pygame.Rect(position[0],
                           position[1],
                           self.WIDTH,
                           self.labels_count * Label.HEIGHT + 2 * self.PADDING)
        super().__init__(
            relative_rect=rect,
            manager=manager,
            starting_layer_height=0)
        self.labels = {}

    def add_caption(self, text=""):
        panel = Label(
            self, pygame.rect.Rect(self.rect.x + self.PADDING, self.rect.y + self.PADDING,
                                   self.WIDTH - 2 * self.PADDING, Label.HEIGHT), text=text)
        self.labels["name"] = panel

    def add_label(self, key="", key_text="", val_text=""):
        key_label = Label(
            self,
            pygame.rect.Rect(self.rect.x + self.PADDING,
                             self.rect.y + Label.HEIGHT * len(self.labels.keys()) + self.PADDING,
                             self.WIDTH // 2 - self.PADDING,
                             Label.HEIGHT),
            text=key_text)
        val_label = Label(
            self,
            pygame.rect.Rect(self.rect.x + self.PADDING + self.WIDTH // 2,
                             self.rect.y + Label.HEIGHT * len(self.labels.keys()) + self.PADDING,
                             self.WIDTH // 2 - 2 * self.PADDING,
                             Label.HEIGHT),
            text=val_text)
        self.labels[key] = [key_label, val_label]
        self.ui_group.add(self.labels[key])


class ResourcesPanel(InfoPanel):
    LABELS_COUNT = 3

    def __init__(self, manager, position):
        self.manager = manager
        super().__init__(manager, position, self.LABELS_COUNT)
        self.add_label(properties.RESOURCES[0]["name"], properties.RESOURCES[0]["visible_name"], "-")
        self.add_label(properties.RESOURCES[1]["name"], properties.RESOURCES[1]["visible_name"], "-")
        self.add_label(properties.RESOURCES[2]["name"], properties.RESOURCES[2]["visible_name"], "-")

    def set_res(self, player):
        self.labels[properties.RESOURCES[0]["name"]][1].set_text(str(player.resources[0]))
        self.labels[properties.RESOURCES[1]["name"]][1].set_text(str(player.resources[1]))
        self.labels[properties.RESOURCES[2]["name"]][1].set_text(str(player.resources[2]))

    def set_back_color(self, color):
        self.background_colour = color


class UnitInfoPanel(InfoPanel):
    LABELS_COUNT = 5

    def __init__(self, manager, position):
        super().__init__(manager, position, self.LABELS_COUNT)
        self.field = None
        self.add_caption("-")
        self.add_label("player", "Игрок", "-")
        self.add_label("position", "Позиция", "-")
        self.add_label("speed", "Очки хода", "-")
        self.add_label("health", "Жизни", "-")

    def set_unit(self, unit: Unit):
        if unit is not None:
            self.labels["player"][1].set_text_color(unit.player.view.color)
        self.set_params(
            properties.UNITS[unit.type]["visible_name"],
            unit.health,
            unit.player.name,
            unit.position,
            unit.current_speed
        )

    def set_params(self, name, cur_health, player_name, position, speed):
        self.labels["name"].set_text(name)
        self.labels["health"][1].set_text(str(cur_health))
        self.labels["position"][1].set_text(str(position))
        self.labels["speed"][1].set_text(str(speed))
        self.labels["player"][1].set_text(str(player_name))


class FieldInfoPanel(InfoPanel):
    LABELS_COUNT = 4

    def __init__(self, manager, position):
        super().__init__(manager, position, self.LABELS_COUNT)
        self.field = None
        self.unit_panels = []
        self.add_caption("-")
        self.add_label("next_ground", "После раскопки", "-")
        self.add_label("resources", "Ресурсы", "-")
        self.add_label("health", "Жизни", "-")

        for i in range(3):
            panel = UnitInfoPanel(
                self.manager, (self.rect.x, self.get_bottom()))
            self.unit_panels.append(panel)

    def set_field(self, field: Field):
        if field is None:
            return
        prop = properties.FIELDS[field.type]
        name = prop["visible_name"]
        health = field.health
        res_name = None
        if prop["resource_type"] is not None:
            res_name = properties.RESOURCES[prop["resource_type"]]["visible_name"]
        next_ground = prop["next_ground"]
        if next_ground is None:
            next_ground = "Туннель"
        else:
            next_ground = properties.FIELDS[next_ground]["visible_name"]
        self.set_params(name, health, res_name, next_ground, field.units)

    def set_params(self, name, cur_health, resource_name, next_ground_name, units=None):
        self.labels["name"].set_text(name)
        self.labels["health"][1].set_text(str(cur_health))
        self.labels["resources"][1].set_text(str(resource_name))
        self.labels["next_ground"][1].set_text(next_ground_name)

        for i in range(3):
            self.unit_panels[i].set_params("-", "-", "-", "-", "-")

        if units is None:
            return

        for i in range(len(units)):
            self.unit_panels[i].set_unit(units[i])

    def get_bottom(self):
        return self.rect.y + self.rect.height + sum([u.rect.height for u in self.unit_panels])


class GameGUI:
    def __init__(self, position, player):
        self.manager = pygame_gui.UIManager(graphics.window.size)
        self.position = position
        self.player = player
        self.field_panel = FieldInfoPanel(self.manager, position)
        pos = position[0], self.field_panel.get_bottom()
        self.res_panel = ResourcesPanel(self.manager, pos)

    def update(self, delta_time):
        self.manager.update(delta_time)

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        graphics.window.screen.fill(
            rect=(graphics.window.width - 250, 0, graphics.window.width, graphics.window.height),
            color=self.player.view.color
        )
        self.manager.draw_ui(graphics.window.screen)
