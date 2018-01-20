from __future__ import absolute_import
import pygame  # In order to install pygame pip3 install pygame should be enough

from threes import *
from io import open

# In case of problems check https://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3

SINGLE_RECT_WIDTH = 80
SINGLE_RECT_HEIGHT = 100
RECT_DISTANCE = 20
ADDITIONAL_INFORMATION_TOP_SPACE = 200

SCORE_SPACE_WIDTH = 200
SCORE_SPACE_HEIGHT = 50

ONE_COLOR = (114, 202, 242)
TWO_COLOR = (241, 103, 128)
NUMBER_COLOR = (255, 255, 255)
EMPTY_COLOR = (187, 217, 217)
BLACK_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (207, 231, 224)
TURN_INDICATOR_COLOR = (63, 220, 84)

FONT_SIZE = 34
FONT = u'Arial'


class Renderer(object):
    def __init__(self):
        self.surfaces = {}
        self.font = pygame.font.SysFont(FONT, FONT_SIZE, bold=True)

    def get_block(self, number):
        u"""
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
            text = self.font.render(u"", 0, EMPTY_COLOR)
        elif number == 1:
            self.surfaces[number].fill(ONE_COLOR)
            text = self.font.render(unicode(number), 1, NUMBER_COLOR)
        elif number == 2:
            self.surfaces[number].fill(TWO_COLOR)
            text = self.font.render(unicode(number), 1, NUMBER_COLOR)
        else:
            self.surfaces[number].fill(NUMBER_COLOR)
            text = self.font.render(unicode(number), 1, BLACK_COLOR)

        self.surfaces[number].blit(text, (SINGLE_RECT_WIDTH // 2 - text.get_width() // 2,
                                          SINGLE_RECT_HEIGHT // 2 - text.get_height() // 2))
        return self.surfaces[number]

    def get_text(self, number):
        return self.font.render(unicode(number), 1, BLACK_COLOR)


class Interface(object):
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
        u"""
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
        u"""
        Shows all the blocks from the model.
        """
        for y in xrange(self.height):
            for x in xrange(self.width):
                self._show_block(x, y, self.model.stateInfo().board[y][x])

    def _show_nexts(self):
        u"""
        Shows the nexts on the interface.
        """
        if self.model.stateInfo().visible_nexts:
            next_panel_width = len(self.model.stateInfo().visible_nexts) * (
                SINGLE_RECT_WIDTH + RECT_DISTANCE) + RECT_DISTANCE
            left_border_pos = self.surface.get_width() // 2 - next_panel_width // 2
            for i, e in enumerate(self.model.stateInfo().visible_nexts):
                pos_x = left_border_pos + RECT_DISTANCE + i * (SINGLE_RECT_WIDTH + RECT_DISTANCE)
                self.surface.blit(self.renderer.get_block(e),
                                  (pos_x, ADDITIONAL_INFORMATION_TOP_SPACE - SINGLE_RECT_HEIGHT - RECT_DISTANCE))

    def _show_score(self):
        u"""
        Shows the score on the interface.
        """
        score = self.model.stateInfo().score
        if score is not None:
            text = self.renderer.get_text(score)
            pos_x = self.surface.get_width() // 2 - SCORE_SPACE_WIDTH // 2
            pos_y = RECT_DISTANCE
            pygame.draw.rect(self.surface, EMPTY_COLOR,
                             (pos_x, pos_y, SCORE_SPACE_WIDTH, SCORE_SPACE_HEIGHT))
            text_pos_x = pos_x + SCORE_SPACE_WIDTH // 2 - text.get_width() // 2
            text_pos_y = pos_y + SCORE_SPACE_HEIGHT // 2 - text.get_height() // 2
            self.surface.blit(text, (text_pos_x, text_pos_y))

    def _show_turn_indicator(self):
        radius = self.surface.get_width() // 10
        pos_x = (self.surface.get_width() // 2 - SCORE_SPACE_WIDTH // 2) // 2
        pos_y = RECT_DISTANCE + SCORE_SPACE_HEIGHT // 2
        pygame.draw.circle(self.surface, TURN_INDICATOR_COLOR, (pos_x, pos_y), radius)

    def redraw(self, my_turn=False):
        u"""
        Redraws the interface. The interface can be displayed on screen later on.
        """
        self.surface.fill(BACKGROUND_COLOR)
        self._show_blocks()
        self._show_nexts()
        self._show_score()
        if my_turn:
            self._show_turn_indicator()


if __name__ == u'__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(u'threes')
    seed = int(time.time())
    random.seed(seed)
    game = Threes()
    file = u''
    if game.save_game:
        filename = getFilename()
        file = open(filename, u'a+')
        file.write(unicode(seed) + u'\n')
        file.flush()
    interface = Interface(game)
    interface.redraw()
    end = False

    screen = pygame.display.set_mode((interface.surface.get_width(), interface.surface.get_height()))

    keys_dict = {
        u"w": MoveEnum.Up,
        u"a": MoveEnum.Left,
        u"s": MoveEnum.Down,
        u"d": MoveEnum.Right,
        u"up": MoveEnum.Up,
        u"down": MoveEnum.Down,
        u"left": MoveEnum.Left,
        u"right": MoveEnum.Right
    }

    pressed_keys = {}

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                if key_pressed == u'escape':
                    end = True
                if key_pressed not in pressed_keys or not pressed_keys[key_pressed]:
                    pressed_keys[key_pressed] = True
                    if key_pressed in keys_dict:
                        m = keys_dict[key_pressed]
                        if game.canMove(m):
                            if game.save_game:
                                saveState(game, m, file)
                            game.turn_counter += 1
                            game.makeMove(m)
                            interface.redraw()
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                pressed_keys[key_pressed] = False
        screen.blit(interface.surface, (0, 0))
        pygame.display.flip()
    if game.save_game:
        file.close()
