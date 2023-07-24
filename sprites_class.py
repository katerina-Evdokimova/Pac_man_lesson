from random import choice

import pygame

from const import SIZE_SP
from data_db.creating_tag import add_inf_game, add_stand_game
from load import load_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None
        self.pos = None
        self.sheet = None
        self.frames = []

    def get_event(self, event):
        pass

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))


class Button(Sprite):
    button = pygame.transform.scale(load_image('button.png', -1), (SIZE_SP * 3, SIZE_SP))

    def __init__(self, button_group, text, x, y, my_font):
        super().__init__(button_group)
        self.image = Button.button
        self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.rect.move(x * SIZE_SP, y * SIZE_SP)
        self.text = text
        self.add_text = my_font.render(text, True, pygame.Color('white'))
        self.level = None

    def update(self, screen, *args) -> None:
        screen.blit(self.add_text, (self.rect.x + 10, self.rect.y + self.rect.height // 4))

        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            print(self.text)
            if self.text == 'Бесконечный':
                self.level = 'inf'
            elif self.text == 'Стандартный':
                self.level = 1
            elif self.text == 'Рейтинг':
                self.level = 'rating'
            elif self.text == 'Меню':
                self.level = 'menu'
            elif self.text == "Стандартный р.":
                self.level = 'stand_table'
            elif self.text == "Бесконечный р.":
                self.level = 'inf_table'
            elif self.text == 'Настройки':
                self.level = 'settings'

    def get_level(self):
        a = self.level
        self.level = None
        return a


class CheckBox(Sprite):
    off = pygame.transform.scale(load_image('check_box_off.png', -1), (SIZE_SP, SIZE_SP // 2))
    on = pygame.transform.scale(load_image('check_box_on.png', -1), (SIZE_SP, SIZE_SP // 2))
    station = (off, on)

    def __init__(self, button_group, x, y):
        super().__init__(button_group)
        self.check = 1
        self.image = CheckBox.station[self.check]
        self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.rect.move(x * SIZE_SP, y * SIZE_SP)

    def update(self, *args) -> None:
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.check += 1
            self.check %= 2
            self.image = CheckBox.station[self.check]

    def set_check(self):
        return self.check


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", -1)]

    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(choice(fire), (scale, scale)))

    def __init__(self, particle_group, pos, dx, dy):
        super().__init__(particle_group)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.4

    def update(self, max_x, max_y, *args):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, max_x * SIZE_SP, max_y * SIZE_SP)):
            self.kill()


class Dot(Sprite):
    dot = pygame.transform.scale(load_image("dot.png", -1), (SIZE_SP, SIZE_SP))
    apple = pygame.transform.scale(load_image("apple.png", -1), (SIZE_SP // 2, SIZE_SP // 2))
    strawberry = pygame.transform.scale(load_image("strawberry.png", -1),
                                        (SIZE_SP // 2, SIZE_SP // 2))

    elem = (dot, apple, strawberry)

    def __init__(self, dot_group, x, y):
        super().__init__(dot_group)
        self.image = choice(Dot.elem)
        self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.rect.move(x, y)
        self.pos = (x // SIZE_SP, y // SIZE_SP)
        self.abs_pos = [self.rect.x, self.rect.y]
        self.score = None
        self.map = []
        self.flag = False

    def update(self, hero_group, SCORE, level, level_map) -> None:
        pass

    def set_map_score(self):
        a, b = self.map, self.score
        self.map = []
        self.score = None
        return a, b

    def __repr__(self):
        return f"<Dot> {'!' * 8 + str(self.flag) + '!' * 8 if self.flag else self.flag} | {self.map[5][4]} | {self.score}\n"


def flag_step(flag):
    flag %= 4
    if flag == 0:
        return [0, 8]
    elif flag == 1:
        return [0, -8]
    elif flag == 2:
        return [8, 0]
    elif flag == 3:
        return [-8, 0]


class Ghost(Sprite):
    columns = 6
    rows = 1

    pink = pygame.transform.scale(load_image("ghost_pink.png", -1),
                                  ((SIZE_SP - 10) * 6, (SIZE_SP - 10)))
    red = pygame.transform.scale(load_image("ghost_red.png", -1),
                                 ((SIZE_SP - 10) * 6, (SIZE_SP - 10)))
    blue = pygame.transform.scale(load_image("ghost_blue.png", -1),
                                  ((SIZE_SP - 10) * 6, (SIZE_SP - 10)))
    orange = pygame.transform.scale(load_image("ghost_orange.png", -1),
                                    ((SIZE_SP - 10) * 6, (SIZE_SP - 10)))
    ghost_color = (pink, red, blue, orange)

    def __init__(self, ghost_group, x, y):
        super().__init__(ghost_group)
        sheet = choice(Ghost.ghost_color)
        self.frames = []
        self.cut_sheet(sheet, Ghost.columns, Ghost.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.abs_pos = [self.rect.x, self.rect.y]
        self.pos = (x // SIZE_SP, y // SIZE_SP)
        self.v = [0, 8]
        self.flag = 0
        self.count = 0

    def move(self, max_x, max_y, block_group, level, level_map):
        self.pos = self.pos[0] % (max_x + 1), self.pos[1] % (max_y + 1)
        x, y = self.pos

        if pygame.sprite.spritecollideany(self, block_group):
            self.flag = choice([0, 1, 2, 3])

        if level == 'inf':
            prev_y = level_map[y - 1][x] == "." if y != 0 else level_map[max_y][x] == "."
            next_y = level_map[y + 1][x] == "." if y != max_y else level_map[0][x] == "."
            prev_x = level_map[y][x - 1] == "." if x != 0 else level_map[y][max_x] == "."
            next_x = level_map[y][x + 1] == "." if x != max_x else level_map[y][0] == "."
        else:
            prev_y = level_map[y - 1][x] == "." if y > 0 else False
            next_y = level_map[y + 1][x] == "." if y < max_y - 1 else False
            prev_x = level_map[y][x - 1] == "." if x > 0 else False
            next_x = level_map[y][x + 1] == "." if x < max_x - 1 else False

        self.v = flag_step(self.flag)

        if prev_y and self.flag == 1 and self.v[1]:
            self.rect.move_ip(0, SIZE_SP // self.v[1])
        elif next_y and self.flag == 0 and self.v[1]:
            self.rect.move_ip(0, SIZE_SP // self.v[1])
        elif prev_x and self.flag == 3 and self.v[0]:
            self.rect.move_ip(SIZE_SP // self.v[0], 0)
        elif next_x and self.flag == 2 and self.v[0]:
            self.rect.move_ip(SIZE_SP // self.v[0], 0)
        else:
            self.flag += 1
            self.flag %= 4

        rect_field = pygame.Rect(x * SIZE_SP, y * SIZE_SP, SIZE_SP,
                                 SIZE_SP)

        rect_x, rect_y = self.rect.x, self.rect.y

        point_1 = rect_field.collidepoint(rect_x + (SIZE_SP - 10) // 2, rect_y)
        point_2 = rect_field.collidepoint(rect_x + (SIZE_SP - 10), rect_y + (SIZE_SP - 10) // 2)
        point_3 = rect_field.collidepoint(rect_x + (SIZE_SP - 10) // 2, rect_y + (SIZE_SP - 10))
        point_4 = rect_field.collidepoint(rect_x, rect_y + (SIZE_SP - 10) // 2)

        point_0 = rect_field.collidepoint(rect_x + (SIZE_SP - 10) // 2,
                                          rect_y + (SIZE_SP - 10) // 2)

        dx, dy = self.v[0], self.v[1]

        if not point_0:
            if dy > 0:
                if not point_1:
                    self.pos = x, y + 1
            elif dy < 0:
                if not point_3:
                    self.pos = x, y - 1
            elif dx > 0:
                if not point_4:
                    self.pos = x + 1, y
            elif dx < 0:
                if not point_2:
                    self.pos = x - 1, y

    def update(self, max_x, max_y, block_group, level, level_map):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        self.move(max_x, max_y, block_group, level, level_map)


class Tile(Sprite):
    tile = pygame.transform.scale(load_image("tile.jpg"), (SIZE_SP - 5, SIZE_SP - 5))

    def __init__(self, block_group, x, y):
        super().__init__(block_group)
        self.image = Tile.tile
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = [self.rect.x, self.rect.y]


def create_particles(position, particle_group):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(particle_group, position, choice(numbers), choice(numbers))


class Pacman(Sprite):
    columns = 3
    rows = 1
    img = pygame.transform.scale(load_image("pacman_hero.png", -1),
                                 ((SIZE_SP - 5) * 3, SIZE_SP - 5))

    def __init__(self, hero_group, x, y):
        super().__init__(hero_group)
        self.sheet = Pacman.img
        self.frames = []
        self.cut_sheet(self.sheet, Pacman.columns, Pacman.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pos = (x // SIZE_SP, y // SIZE_SP)
        self.score = None
        self.level = None
        self.map = None
        self.camera = None

    def update(self, ghost_group, level, SCORE, max_x, particle_group, dot_group, level_map, *args) -> None:

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.score = SCORE
        if pygame.sprite.spritecollideany(self, ghost_group):
            if level != 'GAME OVER':
                if level == 'inf':
                    add_inf_game(SCORE)
                    create_particles((SIZE_SP * ((max_x + 1) // 2),
                                      SIZE_SP * ((max_x + 1) // 2)), particle_group)
                else:
                    add_stand_game(SCORE, level)
                    create_particles((SIZE_SP * self.pos[0], SIZE_SP * self.pos[1]), particle_group)
            self.kill()
            self.score = 'GAME OVER'
        '''Проверяем столкнулся ли персонаж с точкой, если да то начисляем очки'''
        self.map = level_map
        dot_spr = pygame.sprite.spritecollideany(self, dot_group)
        if dot_spr:
            x, y = dot_spr.pos
            print(self.score)
            if self.score != 'GAME OVER':
                self.score += 1
            dot_spr.kill()
            # При бесконечном режиме отмечаем следующие частицы, чтобы впоследствии их заполнить
            if level == 'inf':
                self.map[y][x] = '*'

    def set_score(self):
        return self.score

    def set_map(self):
        return self.map

    def set_camera(self):
        return self.camera

    def move(self, x, y, level, block_group, ghost_group, dot_group, camera):

        if level != 'inf':
            self.pos = (x, y)
            self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2)).move(
                SIZE_SP * self.pos[0], SIZE_SP * self.pos[1])
        else:
            self.camera = camera
            self.camera.dx -= SIZE_SP * (x - self.pos[0])
            self.camera.dy -= SIZE_SP * (y - self.pos[1])

            self.pos = (x, y)

    def rotate(self, movement, max_x, level, max_y):
        x, y = self.pos
        self.frames = []
        if movement == "up":
            image = pygame.transform.rotate(Pacman.img, 90)
            self.cut_sheet(image, Pacman.rows, Pacman.columns)
            self.image = self.frames[self.cur_frame]
        elif movement == "down":
            image = pygame.transform.rotate(Pacman.img, -90)
            self.cut_sheet(image, Pacman.rows, Pacman.columns)
            self.image = self.frames[self.cur_frame]
        elif movement == "left":
            image = pygame.transform.flip(Pacman.img, True, False)
            self.cut_sheet(image, Pacman.columns, Pacman.rows)
            self.image = self.frames[self.cur_frame]
        elif movement == "right":
            image = Pacman.img
            self.cut_sheet(image, Pacman.columns, Pacman.rows)
            self.image = self.frames[self.cur_frame]
        if level != 'inf':
            self.rect = self.rect.move(x * SIZE_SP, y * SIZE_SP)
        else:
            self.rect.x, self.rect.y = (max_x // 2) * SIZE_SP, (
                    max_y // 2) * SIZE_SP


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, max_x, max_y):
        obj.rect.x = (obj.abs_pos[0] + self.dx) % ((max_x + 1) * SIZE_SP)
        obj.rect.y = (obj.abs_pos[1] + self.dy) % ((max_y + 1) * SIZE_SP)

    def update(self):
        self.dx = 0
        self.dy = 0

    def __repr__(self):
        return f"<Camera> {self.dx} {self.dy}"
