from gui.agent_gui import *
from gui.menu import *
from game_manager import *


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        # self.font_name = '8-BIT WONDER.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE, self.GREEN, self.RED = (0, 0, 0), (255, 255, 255), (3, 252, 40), (252, 3, 3)
        self.main_menu = MainMenu(self)

        self.agents = [['random_agents', 2], ['simple_react_agents', 2], ['careful_react_agents', 2]]
        self.steps = 40
        self.options = OptionsMenu(self, self.agents, self.steps)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.setup = True
        self.array_agents_gui = []
        self.game_manager = 0
        self.bg = pygame.image.load("gui/assets/background-game.png")

        self.x_breaking, self.y_breaking = -100,580
        self.players_pos_array = [[230, 320], [360, 320], [500, 320], [155, 400], [560, 400], [230, 490], [360, 490],
                                  [500, 490]]

    def game_loop(self):
        while self.playing:
            if self.setup:
                self.game_manager = GameManager(self.options.states[0][1], self.options.states[1][1],
                                                self.options.states[2][1], self.options.states[-1][1])
                self.setup = False

                c = 0
                for x in self.game_manager.agents_array:
                    self.array_agents_gui.append(
                        Agent_gui(x.type, (self.players_pos_array[c][0], self.players_pos_array[c][1]), self.display, pygame.font.Font(self.font_name, 20), c))
                    c += 1

            self.check_events()

            if self.game_manager.has_ended():
                # TODO
                self.draw_text('Game is Over', 15, 700, 500, self.WHITE)

            if self.ESCAPE_KEY:
                self.playing = False
                pygame.quit()
                exit()

            if self.RIGHT_KEY:
                self.game_manager.step(1)

            if self.UP_KEY:
                self.game_manager.step(10)

            self.display.fill(self.BLACK)
            self.display.blit(self.bg, (0, 0))




            for x in range(len(self.array_agents_gui)):
                if self.array_agents_gui[x].rect.collidepoint(pygame.mouse.get_pos()):
                    self.array_agents_gui[x].hovered = True

                    self.draw_text('CASH AVAILABLE - ' + str(self.game_manager.agents_array[x].get_cash_value()), 15,
                                   600, 5, self.WHITE)
                    self.draw_text('EQUITY - ' + str(self.game_manager.agents_array[x].get_value()), 15, 600, 25,
                                   self.WHITE)
                    self.draw_text('STOCKS VALUE - ' + str(self.game_manager.agents_array[x].get_stock_value()), 15,
                                   600, 45, self.WHITE)
                    self.draw_text('Stock 1 test', 12, 600, 65, self.WHITE)
                    self.draw_text('Stock 2 test', 12, 600, 85, self.WHITE)
                    self.draw_text('Stock 3 test', 12, 600, 105, self.WHITE)

                    c = 20

                    for y in self.game_manager.agents_array[x].get_stocks_owned():
                        self.draw_text(self.game_manager.central_bank.get_stock(y).name, 10, 600, 220 + c, self.WHITE)
                        c += 20


                else:
                    self.array_agents_gui[x].hovered = False
                self.array_agents_gui[x].draw()

            self.draw_text(
                'Current Step - ' + str(self.game_manager.current_step) + '/' + str(self.game_manager.steps_num), 20, 5,
                20, self.WHITE)
            self.draw_text('Stocks', 15, 470, 6, self.WHITE)
            self.draw_text('Price', 15, 547, 6, self.WHITE)
            self.draw_text('Variation', 15, 608, 6, self.WHITE)

            c = 31

            for stock in self.game_manager.central_bank.stocks:
                self.draw_text(stock.name, 12, 470, c, self.WHITE)
                self.draw_text(str(stock.price) + ' €', 12, 553, c, self.WHITE)
                self.draw_text(str(stock.price) + ' %', 12, 620, c, self.GREEN)
                c += 25


            self.draw_text('Breaking News - ' + self.game_manager.get_current_event(), 15, self.x_breaking, self.y_breaking, self.WHITE)
            self.x_breaking +=2
            if self.x_breaking > self.DISPLAY_W:
                self.x_breaking = - 200
            self.draw_text('Mode - ' + self.game_manager.game_mode, 15, 300, 440, self.WHITE)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

        # print results to file for analysis
        # self.game_manager.print_results()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.display.blit(text_surface, text_rect)
