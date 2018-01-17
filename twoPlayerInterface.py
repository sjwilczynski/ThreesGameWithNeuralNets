from gameInterface import *
from twoPlayerGame import *

if __name__ == '__main__':
    games = []
    correct = False
    while not correct:
        game_type = input('Choose game type\n')
        if game_type == 'threes':
            games = [threes.Threes(save_game=False), threes.Threes(save_game=False)]
            correct = True
        elif game_type == '2048':
            games = [g2048.G2048(save_game=False), g2048.G2048(save_game=False)]
            correct = True
        else:
            print('You passed invalid game type - try again')

    seed = int(time.time())
    random.seed(seed)
    moves_dict = {"w": MoveEnum.Up,
                  "a": MoveEnum.Left,
                  "s": MoveEnum.Down,
                  "d": MoveEnum.Right}
    valid_inputs = ['w', 'a', 's', 'd', 'up', 'left', 'down', 'right']
    players = ['Player1', 'Player2']
    curr_player = 0

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption(game_type)
    interfaces = list(map(lambda x: Interface(x), games))

    width = sum(interface.surface.get_width() for interface in interfaces)
    height = max(interface.surface.get_height() for interface in interfaces)

    screen = pygame.display.set_mode((width,height))

    end = False
    pressed_keys = {}

    for i, intf in enumerate(interfaces):
        intf.redraw(curr_player == i)

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
                    user_input = key_pressed
                    if user_input in valid_inputs:
                        ind = valid_inputs.index(user_input)
                        i = int(ind > 3)
                        move = moves_dict[valid_inputs[ind - 4] if i else valid_inputs[ind]]
                        if games[i].canMove(move):
                            games[i].turn_counter += 1
                            games[i].makeMove(move)
                            curr_player = (curr_player + 1) % 2
                if not is_any_move_valid(games[0], games[1], moves_dict):
                    end = True
                for i, intf in enumerate(interfaces):
                    intf.redraw(curr_player == i)
            if event.type == pygame.KEYUP:
                key_pressed = pygame.key.name(event.key)
                pressed_keys[key_pressed] = False
        x = 0
        for interface in interfaces:
            screen.blit(interface.surface, (x, 0))
            x += interface.surface.get_width()
        pygame.display.flip()
    # TODO Don't close the window immediately after players are out of moves
