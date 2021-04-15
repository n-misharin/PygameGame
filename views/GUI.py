import pygame_gui
import pygame


class PanelLabel(pygame_gui.elements.UITextBox):
    def __init__(self, parent, delta=(0, 0), text="", width=None):
        if width is None:
            width = parent.rect.w
        self.height = 32
        parent = parent
        rect = pygame.Rect((0, 0), (width - parent.padding * 2, self.height))
        rect.topleft = (parent.rect.x + parent.padding + delta[0], parent.padding + delta[1])

        super().__init__(
            wrap_to_height=False,
            relative_rect=rect,
            manager=parent.manager,
            parent_element=parent,
            html_text=f"""<font size='{(self.height - 2) / 10}'>{text}</font>""",
            anchors={
                "left": "left",
                "right": "left",
                "top": "top",
                "bottom": "bottom"
            })


class UnitInfoPanel(pygame_gui.elements.UIPanel):
    LABEL_HEIGHT = 32
    UNIT_PARAMETER_LABELS = ["speed", "health", "player"]
    WIDTH = 250
    PADDING = 10

    def __init__(self, manager, position=(500, 0)):
        self.padding = self.PADDING
        self.unit_parameters = [''] * len(self.UNIT_PARAMETER_LABELS)

        height = (len(self.UNIT_PARAMETER_LABELS) + 1) * self.LABEL_HEIGHT + self.padding * 2
        width = self.WIDTH

        rect = pygame.Rect(position, (width, height))

        super().__init__(
            relative_rect=rect,
            manager=manager,
            starting_layer_height=0)

        self.manager = manager
        self.labels = []
        self.init_children()

    def init_children(self):
        self.labels = []
        self.add_label(PanelLabel(self, delta=(0, 0), text="Персонаж"))
        for i in range(1, len(self.UNIT_PARAMETER_LABELS) + 1):
            self.add_label(PanelLabel(self, delta=(0, self.LABEL_HEIGHT * i), text=self.UNIT_PARAMETER_LABELS[i - 1], width=self.rect.w // 2))
            self.add_label(PanelLabel(self, delta=(self.rect.w // 2, self.LABEL_HEIGHT * i), text=self.unit_parameters[i - 1], width=self.rect.w // 2))

    def add_label(self, label):
        self.labels.append(label)

    def set_unit_parameters(self, values_list):
        self.unit_parameters = values_list[:]
        self.init_children()


class GraphicUserInterface:
    def __init__(self, win_size):
        self.window_surface = pygame.display.set_mode(win_size)
        self.manager = pygame_gui.UIManager(win_size)

    def init_widgets(self):
        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Say Hello',
                                                    manager=self.manager)
        unit_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((600, 0), (200, 200)), manager=self.manager,
                                                 starting_layer_height=1)
        unit_type_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((650, 30), (50, 60)),
                                                      manager=self.manager, parent_element=unit_panel, text="LOL")
