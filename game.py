import sys
from random import sample

import pygame

from data_db import db_session
from data_db.creating_tag import add_inf_game, add_stand_game
from data_db.inf_game import InfGame
from data_db.stand_game import StandGame
from level_game import load_level
from load import load_image
from sprites_class import Button, Camera, Dot, Tile, Pacman, Ghost, CheckBox

import pygame_gui  # pip install pygame_gui


class Game:
    SIZE_SP = None  # 50
    TIME = 1500
    FPS = 10
    LEVEL = None

    SCORE = 0

    max_x = 10
    max_y = 10
    level_map = None
    hero = None
    camera = None

    def __init__(self, count_level, size_sprites):
        '''

        :param count_level: количество загруженных уровней
        :param size_sprites: размер спрайтов в игре
        '''
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.music.load("sounds/game.mp3")
        self.my_font = pygame.font.SysFont('segoeui', 20, 'bolt')
        self.SIZE_SP = size_sprites
        self.LEVEL = count_level

        self.ghost_group = pygame.sprite.Group()
        self.hero_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.dot_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()

        self.screen = None
        self.size_rect_screen = None
        self.update_size_screen()

        self.level = None

        self.button_group = pygame.sprite.Group()
        self.check = CheckBox(self.button_group, self.max_x - 4, self.max_y // 2)

        self.manager = pygame_gui.UIManager(self.size_rect_screen)
        self.menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            ((self.max_x // 2) * self.SIZE_SP, (1 + 7.8) * self.SIZE_SP, self.SIZE_SP * 3, self.SIZE_SP)),
            text='Меню')

        self.sounds_flag = True

        self.game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')
        self.up_level_sound = pygame.mixer.Sound('sounds/up_level.mp3')

    def get_sounds(self):
        self.sounds_flag = not self.sounds_flag

    def generate_level(self, levels):
        pacman, x, y, count_local = None, None, None, 0
        for y in range(len((levels))):
            for x in range(len(levels[y])):
                if levels[y][x] == '.':
                    Dot(self.dot_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    count_local += 1
                elif levels[y][x] == '#':
                    Tile(self.block_group, x * self.SIZE_SP, y * self.SIZE_SP)
                elif levels[y][x] == '@':
                    pacman = Pacman(self.hero_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    Dot(self.dot_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    levels[y][x] = "."
                    count_local += 1
                elif levels[y][x] == '&':
                    Ghost(self.ghost_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    Dot(self.dot_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    levels[y][x] = "."
                    count_local += 1
        return pacman, x, y, count_local + self.SCORE

    def update_size_screen(self):
        self.size_rect_screen = (self.max_x + 1) * self.SIZE_SP, (self.max_y + 1) * self.SIZE_SP
        self.screen = pygame.display.set_mode(self.size_rect_screen)

    def main_sound(self):
        if self.sounds_flag:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def start_screen(self):
        self.SCORE = 0

        self.update_size_screen()

        button_group = pygame.sprite.Group()
        pygame.display.set_caption('Меню')
        x, y = 2, 2

        for text in ['Бесконечный', "Стандартный", "Рейтинг"]:
            Button(button_group, text, x, y, self.my_font)
            x, y = x + 3, y
        Button(button_group, 'Настройки', x - 6, y + 1.5, self.my_font)

        self.level = None
        screen_start = True
        while screen_start:
            self.screen.fill(pygame.Color('white'))
            button_group.draw(self.screen)
            button_group.update(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                button_group.draw(self.screen)
                button_group.update(self.screen, event)
                b_sprite = [el for el in button_group.sprites() if el.level != None]
                if b_sprite:
                    self.level = b_sprite[0].get_level()

                if event.type == pygame.QUIT:
                    screen_start = False
                    self.terminate()

            if self.level == 'inf':
                self.level = 'inf'
                screen_start = False
                pygame.mixer.music.play(-1)
                self.ghost_group = pygame.sprite.Group()
                self.hero_group = pygame.sprite.Group()
                self.block_group = pygame.sprite.Group()
                self.dot_group = pygame.sprite.Group()

                self.level_map = load_level(f"level_inf.map")
                self.hero, self.max_x, self.max_y, count = self.generate_level(self.level_map)
                self.camera = Camera()
                self.update_size_screen()
                self.screen.fill(0)
                self.camera.update()

                self.start_game_inf()
            elif self.level == 1:
                while self.level and self.level <= self.LEVEL:
                    self.ghost_group = pygame.sprite.Group()
                    self.hero_group = pygame.sprite.Group()
                    self.block_group = pygame.sprite.Group()
                    self.dot_group = pygame.sprite.Group()

                    self.level_map = load_level(f"level_{self.level}.map")
                    self.hero, self.max_x, self.max_y, count = self.generate_level(self.level_map)
                    self.level = self.start_game(count)
                add_stand_game(self.SCORE, self.level - 1)
                screen_start = False
                self.sounds_flag = False
                self.main_sound()
                self.start_screen()
            elif self.level == 'rating':
                screen_start = False
                self.rating_screen()
            elif self.level == 'settings':
                screen_start = False
                self.setting_screen()

    def terminate(self):
        if self.level:
            if self.level == 'inf':
                add_inf_game(self.SCORE)
            elif self.level >= 1:
                add_stand_game(self.SCORE, self.level)
        pygame.quit()
        sys.exit

    def update_screen(self, screen, text, dot=True, ghost=True, hero=True, block=True, particle=True):
        # screen.fill(0)
        if dot:
            self.dot_group.draw(screen)
            self.dot_group.update(self.hero_group, self.SCORE, self.level, self.level_map)
        if ghost:
            self.ghost_group.draw(screen)
            self.ghost_group.update(self.max_x, self.max_y, self.block_group, self.level, self.level_map)
        if hero:
            self.hero_group.draw(screen)
            self.hero_group.update(self.ghost_group, self.level, self.SCORE, self.max_x, self.particle_group,
                                   self.dot_group, self.level_map)
            self.SCORE = self.hero.set_score()
            self.level_map = self.hero.set_map()
        if block:
            self.block_group.draw(screen)
        if particle:
            self.particle_group.draw(screen)
            self.particle_group.update(self.max_x, self.max_y)

        screen.blit(text, (self.max_x * self.SIZE_SP - text.get_width() + 10, 10))

    def generate_dot(self):
        for y in range(sample([0, 1, 2], 1)[0], len(self.level_map), 2):
            for x in range(sample([0, 1, 2], 1)[0], len(self.level_map[y]), 2):
                if self.level_map[y][x] == '*':
                    Dot(self.dot_group, x * self.SIZE_SP, y * self.SIZE_SP)
                    self.level_map[y][x] = '.'

    def event_key_down(self, event):
        if event.key == pygame.K_UP:
            self.move("up")
        elif event.key == pygame.K_DOWN:
            self.move("down")
        elif event.key == pygame.K_LEFT:
            self.move("left")
        elif event.key == pygame.K_RIGHT:
            self.move("right")

    def start_game(self, count):
        pygame.display.set_caption(f'Стандартный режим. Уровень: {self.level}')
        self.update_size_screen()

        game = True
        pause = False
        clock = pygame.time.Clock()
        time = False
        self.main_sound()
        while game:
            self.screen.fill(0)
            text = self.my_font.render(f'SCORE: {self.SCORE}', False, pygame.Color('white'))

            if not pause:

                self.update_screen(self.screen, text)
                if time and time_now <= pygame.time.get_ticks():
                    self.game_over_screen()
                    game = False
                pygame.display.flip()
                clock.tick(self.FPS)
                if count == self.SCORE:
                    if self.check.set_check():
                        self.up_level_sound.play()
                    return self.level + 1
                if self.SCORE == 'GAME OVER':
                    if not time:
                        if self.check.set_check():
                            self.game_over_sound.play()
                        self.sounds_flag = False
                        self.main_sound()
                        time_now = pygame.time.get_ticks() + self.TIME
                        time = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.sounds_flag = False
                        self.main_sound()
                        game = False
                        self.terminate()
                    elif event.type == pygame.KEYDOWN:
                        self.event_key_down(event)
                        if event.key == pygame.K_p:
                            self.sounds_flag = False
                            pause = True
                        elif event.key == pygame.K_ESCAPE:
                            add_stand_game(self.SCORE, self.level)
                            self.sounds_flag = False
                            self.main_sound()
                            game = False
                            self.start_screen()
            else:
                pause = self.pause_screen()

    def start_game_inf(self):
        game = True
        pause = False
        clock = pygame.time.Clock()
        time = False
        pygame.display.set_caption('Бесконечный режим')
        self.main_sound()
        while game:
            self.screen.fill(0)
            text = self.my_font.render(f"SCORE: {self.SCORE}", False, pygame.Color('white'))
            if not pause:
                self.update_screen(self.screen, text)
                pygame.display.flip()
                clock.tick(self.FPS)
                if time and time_now <= pygame.time.get_ticks():
                    self.game_over_screen()
                    game = False

                if self.SCORE == 'GAME OVER':
                    if not time:
                        if self.check.set_check():
                            self.game_over_sound.play()
                        self.sounds_flag = False
                        self.main_sound()
                        time_now = pygame.time.get_ticks() + self.TIME
                        time = True
                elif self.SCORE % 10 == 0:
                    self.generate_dot()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game = False
                        self.sounds_flag = False
                        self.main_sound()
                        self.terminate()
                    elif event.type == pygame.KEYDOWN:
                        self.event_key_down(event)
                        if event.key == pygame.K_p:
                            pause = True
                        elif event.key == pygame.K_ESCAPE:
                            add_inf_game(self.SCORE)
                            game = False
                            self.sounds_flag = False
                            self.main_sound()
                            self.start_screen()
            else:
                pause = self.pause_screen()

    def rating_screen(self):
        x, y = 2, 1
        self.screen.fill(0)
        inf_font = pygame.font.SysFont('segoeui', 13)
        button_group = pygame.sprite.Group()

        for text in ['Общий рейтинг', "Стандартный р.", "Бесконечный р."]:
            Button(button_group, text, x, y, self.my_font)
            x, y = x + 3.5, y

        # Работа с таблицами
        db_sess = db_session.create_session()
        all_list = []
        inf_game = db_sess.query(InfGame).all()
        all_list.extend(inf_game)
        stand_game = db_sess.query(StandGame).all()
        all_list.extend(stand_game)
        all_list = sorted(all_list, key=lambda x: x.create_date, reverse=True)
        db_sess.close()

        clock = pygame.time.Clock()

        rating = True
        while rating:

            time_delta = clock.tick(60) / 1000.0
            self.screen.fill(0)
            for event in pygame.event.get():
                self.manager.process_events(event)

                button_group.draw(self.screen)
                button_group.update(self.screen, event)
                b_sprite = [el for el in button_group.sprites() if el.level != None]
                if b_sprite:
                    self.level = b_sprite[0].get_level()

                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.menu_button:
                        rating = False
                        self.start_screen()
                        self.manager.clear_and_reset()

            rating_table = []

            if self.level == 'stand_table':
                rating_table = list(reversed(stand_game))
            elif self.level == 'inf_table':
                rating_table = list(reversed(inf_game))
            elif self.level == 'all_table' or self.level not in ['stand_table', 'inf_table']:
                rating_table = all_list

            count = 1
            text = self.my_font.render(
                f'id | Режим | Дата/время | Очки | ~Уровень',
                True, pygame.Color("white"))
            count += 1
            self.screen.blit(text, (2 * self.SIZE_SP, 2 * self.SIZE_SP))
            x_r, y_r = 2, 3
            for el in rating_table[:6]:
                text = self.my_font.render(
                    f'{count} | {"Бесконечный" if "InfGame" in el.__class__.__name__ else "Стандартный"} | {str(el.create_date)[:-7]} | {el.score} {"| " + str(el.level) if el.__class__.__name__ == "StandGame" else ""}',
                    True, pygame.Color("white"))
                count += 1
                self.screen.blit(text, (x_r * self.SIZE_SP, y_r * self.SIZE_SP))
                y_r += 1
            self.screen.blit(
                inf_font.render('Для сортировки по очкам нажмите стрелки(PgUp - по возрастанию, PgDn - по убыванию)',
                                True, pygame.Color('white')), (10, 10))

            self.manager.update(time_delta)
            button_group.draw(self.screen)
            button_group.update(self.screen)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def setting_screen(self):
        self.screen.fill(0)

        settings = True
        clock = pygame.time.Clock()

        while settings:
            time_delta = clock.tick(60) / 1000.0
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(
                self.my_font.render('Звук: ',
                                    True, pygame.Color('black')),
                ((self.max_x - 6) * self.SIZE_SP, (self.max_y // 2 + 0.1) * self.SIZE_SP))

            self.button_group.draw(self.screen)
            self.button_group.update()
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                self.manager.process_events(event)

                self.button_group.draw(self.screen)
                self.button_group.update(event)
                self.sounds_flag = self.check.set_check()

                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.menu_button:
                        settings = False
                        self.start_screen()
                        self.manager.clear_and_reset()

    def pause_screen(self):
        pause = True
        self.sounds_flag = False
        self.main_sound()
        while pause:
            text_pause = self.my_font.render(f'PAUSE', False, pygame.Color('white'))
            self.update_screen(self.screen, text_pause, False, False, False, False, False)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.sounds_flag = True if self.check.set_check() else False
                        pause = False
        self.main_sound()
        return pause

    def game_over_screen(self):
        pygame.display.set_caption('Проигрыш')
        game_over_img = pygame.transform.scale(load_image('game_over.png', -1),
                                               self.size_rect_screen)
        self.update_size_screen()
        start = True

        while start:
            self.screen.fill(0)
            self.screen.blit(game_over_img, (0, 0, self.max_x + 1, self.max_y + 1))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    start = False
        self.start_screen()

    def move(self, movement):
        x, y = self.hero.pos
        if self.level == 'inf':
            prev_y = (self.level_map[y - 1][x] in ".*", y - 1) if y != 0 else (
                self.level_map[self.max_y][x] in ".*", self.max_y)
            next_y = (self.level_map[y + 1][x] in ".*", y + 1) if y != self.max_y else (self.level_map[0][x] in ".*", 0)
            prev_x = (self.level_map[y][x - 1] in ".*", x - 1) if x != 0 else (
                self.level_map[y][self.max_x] in ".*", self.max_x)
            next_x = (self.level_map[y][x + 1] in ".*", x + 1) if x != self.max_x else (self.level_map[y][0] in ".*", 0)
        else:
            prev_y = (self.level_map[y - 1][x] == ".", y - 1) if y > 0 else (False, 0)
            next_y = (self.level_map[y + 1][x] == ".", y + 1) if y < self.max_y - 1 else (False, 0)
            prev_x = (self.level_map[y][x - 1] == ".", x - 1) if x > 0 else (False, 0)
            next_x = (self.level_map[y][x + 1] == ".", x + 1) if x < self.max_x - 1 else (False, 0)

        args = (self.level, self.block_group, self.ghost_group, self.dot_group, self.camera)
        args2 = (self.max_x, self.level, self.max_y)
        if movement == "up":
            if prev_y[0]:
                self.hero.move(x, prev_y[1], *args)
                self.hero.rotate(movement, *args2)
        elif movement == "down":
            if next_y[0]:
                self.hero.move(x, next_y[1], *args)
                self.hero.rotate(movement, *args2)
        elif movement == "left":
            if prev_x[0]:
                self.hero.move(prev_x[1], y, *args)
                self.hero.rotate(movement, *args2)
        elif movement == "right":
            if next_x[0]:
                self.hero.move(next_x[1], y, *args)
                self.hero.rotate(movement, *args2)
        if self.level == 'inf':
            self.camera = self.hero.set_camera()
            args = (self.max_x, self.max_y)
            for sprite in self.block_group:
                self.camera.apply(sprite, *args)
            for sprite in self.ghost_group:
                self.camera.apply(sprite, *args)
                # sprite.pos = sprite.pos[0] + camera.dx, sprite.pos[1] + camera.dy
            for sprite in self.dot_group:
                self.camera.apply(sprite, *args)
            print(self.camera)
