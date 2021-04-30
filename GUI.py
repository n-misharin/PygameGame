import pygame_gui
import pygame
from model import Field, Unit
import properties
import graphics


class Label(pygame_gui.elements.UILabel):
    HEIGHT = 26
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


class UpPanel(pygame_gui.elements.UIPanel):
    HEIGHT = 40
    PADDING = 10

    def __init__(self, manager, player, position=(0, 0)):
        self.player = player
        self.manager = manager
        self.labels = []
        rect = pygame.rect.Rect(position[0], position[1],
                                graphics.window.width - InfoPanel.WIDTH, self.HEIGHT)
        super().__init__(
            relative_rect=rect,
            starting_layer_height=0,
            manager=self.manager
        )
        self._add_label(text="Ходит:")
        self._add_label(
            width=200,
            text=self.player.name,
            bg_color=pygame.color.Color(0, 0, 0),
            text_color=self.player.view.color)
        self._add_label(
            text=properties.RESOURCES[0]["visible_name"] + ':')
        self._add_label(
            text=str(self.player.resources[0]),
            bg_color=pygame.color.Color(0, 0, 0))

        self._add_label(
            text=properties.RESOURCES[1]["visible_name"] + ':')
        self._add_label(
            text=str(self.player.resources[1]),
            bg_color=pygame.color.Color(0, 0, 0))

        self._add_label(
            text=properties.RESOURCES[2]["visible_name"] + ':')
        self._add_label(
            text=str(self.player.resources[2]),
            bg_color=pygame.color.Color(0, 0, 0))

    def _add_label(self,
                   width=70,
                   text="",
                   bg_color=None,
                   text_color=pygame.color.Color(255, 255, 255)):
        rect = pygame.rect.Rect(
            self.rect.x + self.PADDING + self.PADDING * len(self.labels) + sum([lbl.rect.width for lbl in self.labels]),
            self.rect.y + 2 * self.PADDING // 3,
            width,
            Label.HEIGHT)

        lbl = Label(self, rect)
        self.labels.append(lbl)

        if bg_color is not None:
            lbl.bg_colour = bg_color

        lbl.set_text_color(text_color)
        lbl.set_text(text)


class ButtonsPanel(pygame_gui.elements.UIPanel):
    PADDING = 10
    BUTTON_SIZE_W = 50
    BUTTON_SIZE_H = 40
    BUTTONS_IN_ROW = 4
    HEIGHT = 140

    def __init__(self, manager, position):
        self.manager = manager
        self.buttons = []
        super().__init__(
            relative_rect=pygame.rect.Rect(
                position[0], position[1],
                InfoPanel.WIDTH, self.HEIGHT),
            manager=self.manager,
            starting_layer_height=0)
        self._add_button("1")
        self._add_button("2")
        self._add_button("3")
        self._add_button("4")
        self._add_button("5")
        self._add_button("6")
        self._add_button("7")
        self._add_button("8")

        self.turn_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.rect.Rect(
                self.rect.x + self.PADDING,
                self.rect.y + self.rect.height - self.PADDING - self.BUTTON_SIZE_H,
                self.rect.width - self.PADDING * 2,
                self.BUTTON_SIZE_H),
            text="Закончить ход",
            manager=self.manager,
        )
        #self.turn_button.disable()
        #print(self.turn_button.pressed)

    def _add_button(self, text=""):
        btn_cnt = len(self.buttons)
        self.buttons.append(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.rect.Rect(
                    self.rect.x + self.PADDING +
                    self.PADDING * (btn_cnt % self.BUTTONS_IN_ROW) +
                    sum([btn.rect.width for btn in self.buttons[:btn_cnt % self.BUTTONS_IN_ROW]]),

                    self.rect.y + self.PADDING + self.BUTTON_SIZE_H * (btn_cnt // self.BUTTONS_IN_ROW),
                    self.BUTTON_SIZE_W,
                    self.BUTTON_SIZE_H),
                text=text,
                manager=self.manager)
        )


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

        self.res_panel = ButtonsPanel(self.manager, pos)
        self.up_panel = UpPanel(self.manager, player)

    def update(self, delta_time):
        self.manager.update(delta_time)
        if self.res_panel.turn_button.pressed:
            print(1)

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        graphics.window.screen.fill(
            rect=(graphics.window.width - 250, 0, graphics.window.width, graphics.window.height),
            color=self.player.view.color
        )
        self.manager.draw_ui(graphics.window.screen)
