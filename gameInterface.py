import pygame  # In order to install pygame pip3 install pygame should be enough

from threes import *

SINGLE_RECT_WIDTH = 80
SINGLE_RECT_HEIGHT = 100
RECT_DISTANCE = 20
ADDITIONAL_INFORMATION_TOP_SPACE = 170

SCORE_SPACE_WIDTH = 150
SCORE_SPACE_HEIGHT = 80

SCORE_POS_X = 10
SCORE_POS_Y = 20

ONE_COLOR = (114, 202, 242)
TWO_COLOR = (241, 103, 128)
NUMBER_COLOR = (255, 255, 255)
EMPTY_COLOR = (187, 217, 217)
BLACK_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (207, 231, 224)

FONT_SIZE = 34
FONT = 'Arial'


class Renderer:
    def __init__(self):
        self.surfaces = {}
        self.font = pygame.font.SysFont(FONT, FONT_SIZE, bold=True)

    def get_block(self, number):
        """
        Handles creation of blocks in the interface. Makes sure each block is created only once.
        :param number: The number identifying the block.
        :return: The surface to display.
        """
        if number in self.surfaces:
            return self.surfaces[number]

        self.surfaces[number] = pygame.Surface((SINGLE_RECT_WIDTH, SINGLE_RECT_HEIGHT))
        text = None
        if number == 0:
            self.surfaces[number].fill(EMPTY_COLOR)
            text = self.font.render("", 0, EMPTY_COLOR)
        elif number == 1:
            self.surfaces[number].fill(ONE_COLOR)
            text = self.font.render(str(number), 1, NUMBER_COLOR)
        elif number == 2:
            self.surfaces[number].fill(TWO_COLOR)
            text = self.font.render(str(number), 1, NUMBER_COLOR)
        else:
            self.surfaces[number].fill(NUMBER_COLOR)
            text = self.font.render(str(number), 1, BLACK_COLOR)

        self.surfaces[number].blit(text, (SINGLE_RECT_WIDTH // 2 - text.get_width() // 2,
                                          SINGLE_RECT_HEIGHT // 2 - text.get_height() // 2))
        return self.surfaces[number]

    def get_text(self, number):
        return self.font.render(str(number), 1, BLACK_COLOR)


class Interface:
    def __init__(self, model):
        self.width = model.width
        self.height = model.height
        self.model = model

        window_width = self.width * SINGLE_RECT_WIDTH + (self.width + 1) * RECT_DISTANCE
        window_height = self.height * SINGLE_RECT_HEIGHT + (self.height + 1) * RECT_DISTANCE + \
                                                                ADDITIONAL_INFORMATION_TOP_SPACE
        self.surface = pygame.Surface((window_width, window_height))

        self.renderer = Renderer()

    def _show_block(self, x, y, number):
        """
        Shows the block on position x,y with given number.
        :param x: Horizontal position. From 0 to model.width
        :param y: Vertical position. From 0 to model.height
        :param number: The number to display
        """
        block_surface = self.renderer.get_block(number)
        draw_pos_x = RECT_DISTANCE + x * (SINGLE_RECT_WIDTH + RECT_DISTANCE)
        draw_pos_y = ADDITIONAL_INFORMATION_TOP_SPACE + \
                     RECT_DISTANCE + y * (SINGLE_RECT_HEIGHT + RECT_DISTANCE)
        self.surface.blit(block_surface, (draw_pos_x, draw_pos_y))

    def _show_blocks(self):
        """
        Shows all the blocks from the model.
        """
        for y in range(self.height):
            for x in range(self.width):
                self._show_block(x, y, self.model.stateInfo().board[y][x])

    def _show_nexts(self):
        """
        Shows the nexts in the middle of ADDITIONAL_INFORMATION_TOP_SPACE.
        """
        if self.model.stateInfo().visible_nexts:
            next_panel_width = len(self.model.stateInfo().visible_nexts) * (
                SINGLE_RECT_WIDTH + RECT_DISTANCE) + RECT_DISTANCE
            left_border_pos = self.surface.get_width() // 2 - next_panel_width // 2
            for i, e in enumerate(self.model.stateInfo().visible_nexts):
                pos_x = left_border_pos + RECT_DISTANCE + i * (SINGLE_RECT_WIDTH + RECT_DISTANCE)
                self.surface.blit(self.renderer.get_block(e),
                                  (pos_x, ADDITIONAL_INFORMATION_TOP_SPACE // 2 - SINGLE_RECT_HEIGHT // 2))

    def _show_score(self):
        score = self.model.stateInfo().score
        if score:
            text = self.renderer.get_text(score)
            pygame.draw.rect(self.surface,EMPTY_COLOR,(SCORE_POS_X, SCORE_POS_Y, SCORE_SPACE_WIDTH, SCORE_SPACE_HEIGHT))
            text_pos_x = SCORE_POS_X + SCORE_SPACE_WIDTH // 2 - text.get_width() // 2
            text_pos_y = SCORE_POS_Y + SCORE_SPACE_HEIGHT // 2 - text.get_height() // 2
            self.surface.blit(text, (text_pos_x,text_pos_y))



    def redraw(self):
        """
        Redraws the interface. The interface can be displayed on screen later on.
        """
        self.surface.fill(BACKGROUND_COLOR)
        self._show_blocks()
        self._show_nexts()
        self._show_score()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('threes')
    game = Threes()
    filename = getFilename()
    interface = Interface(game)
    interface.redraw()
    end = False

    screen = pygame.display.set_mode((interface.surface.get_width(), interface.surface.get_height()))

    keys_dict = {
        "w": MoveEnum.Up,
        "a": MoveEnum.Left,
        "s": MoveEnum.Down,
        "d": MoveEnum.Right,
        "up": MoveEnum.Up,
        "down": MoveEnum.Down,
        "left": MoveEnum.Left,
        "right": MoveEnum.Right
    }

    pressed_keys = {}

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                if key_pressed == 'escape':
                    end = True
                if key_pressed not in pressed_keys or not pressed_keys[key_pressed]:
                    pressed_keys[key_pressed] = True
                    if key_pressed in keys_dict:
                        m = keys_dict[key_pressed]
                        if game.canMove(m):
                            if game.save_game:
                                saveState(game, m.value, filename)
                            game.turn_counter += 1
                            game.makeMove(m)
                            interface.redraw()
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                pressed_keys[key_pressed] = False
        screen.blit(interface.surface, (0, 0))
        pygame.display.flip()
