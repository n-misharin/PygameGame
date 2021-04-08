import pygame_gui
import pygame


class PanelLabel(pygame_gui.elements.UILabel):
    def __init__(self, parent, delta=(0, 0), text=""):
        parent = parent
        rect = pygame.Rect((0, 0), (parent.rect.w - parent.padding * 2, 20))
        rect.topleft = (parent.rect.x + parent.padding + delta[0], parent.padding + delta[1])

        super().__init__(
            relative_rect=rect,
            manager=parent.manager,
            parent_element=parent,
            text=text,
            anchors={
                "left": "left",
                "right": "left",
                "top": "top",
                "bottom": "bottom"
            })

        self.ui_theme.load_theme("themes\label.json")


class UnitInfoPanel(pygame_gui.elements.UIPanel):
    def __init__(self, manager, rect=pygame.Rect((500, 0), (100, 100))):
        super().__init__(
            relative_rect=rect,
            manager=manager,
            starting_layer_height=0)
        self.manager = manager
        self.padding = 10

        self.labels = []

        self.init_children()

    def init_children(self):
        self.add_label(PanelLabel(self, text="Привет"))
        self.add_label(PanelLabel(self, delta=(0, 30), text="1"))
        self.add_label(PanelLabel(self, delta=(0, 60), text="123"))

    def add_label(self, label):
        self.labels.append(label)


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
