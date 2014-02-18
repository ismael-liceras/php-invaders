import pygame
from pygame.locals import *
from enemy import Enemy
from option import Option
from enemybox import EnemyBox
from gameconfig import GameConfig
from prisoner import Prisoner
from specialitem import SpecialItem
import random


class StageGenerator():

    MAX_ENEMIES_PER_ROW = 7
    ENEMY_SPRITE_WIDTH = 64
    ENEMY_SPRITE_HEIGHT = 64
    ENEMY_ROW_GAP = 20
    ENEMY_ROW_TOP_ADDITIONAL_MARGIN = 20
    PRISONER_SPRITE_WIDTH = 32

    def __init__(self):
        self.stage = None
        self.background = None
        self.subtitle_font_color = (255, 255, 255)
        self.reset()

    def reset(self):
        self.stage = 0
        self.refresh_background()

    def get_background(self):
        if self.background is None:
            self.background = pygame.image.load("data/stage1_bg.png").convert()
        return self.background

    def get_ready_to_next_stage(self, score=None, stage_score=None, bonus=None):
        self.stage += 1
        self.refresh_background()
        self.show_stage_banner(score, stage_score, bonus)
        pygame.time.set_timer(USEREVENT + 1, 0)
        pygame.time.set_timer(USEREVENT + 2, 3000)

    def start_next_stage(self):
        # Se generan las posiciones al azar de los enemigos en "enemies_bucket"
        enemies_sd = GameConfig.get_enemies(self.stage)
        enemies_bucket = []
        for (enemy_type, enemy_quantity) in enemies_sd:
            for x in range(0, enemy_quantity):
                enemies_bucket.append(enemy_type)
        random.shuffle(enemies_bucket)
        total_enemies = len(enemies_bucket)

        #Se calculan los objetos especiales
        items_sd = GameConfig.get_items(self.stage)
        items_bucket = []
        for (item_type, item_quantity) in items_sd:
            for x in range(0, item_quantity):
                items_bucket.append(item_type)
        while len(items_bucket) < total_enemies:
            items_bucket.append(None)
        random.shuffle(items_bucket)

        # Creando los sprites de los enemigos
        great_rect = None
        enemy_shoots = pygame.sprite.RenderPlain()
        enemies = pygame.sprite.RenderPlain()
        x = -1
        for etype in enemies_bucket:
            x += 1
            start_position = self.get_start_position_for_enemy(x, total_enemies)
            enemy = Enemy((etype - 1), items_bucket[x], start_position, enemy_shoots)
            enemy.add(enemies)
            if great_rect is None:
                great_rect = enemy.get_rect().copy()
            else:
                great_rect.union_ip(enemy.get_rect())
        enemy_box = EnemyBox(great_rect, GameConfig.get_move(self.stage))
        for e in enemies:
            e.set_enemy_box(enemy_box)

        # Se generan los prisioneros
        prisoners = pygame.sprite.RenderPlain()
        nprisoners = GameConfig.get_prisoners(self.stage)
        screen = pygame.display.get_surface()
        gap = (screen.get_width() - (self.PRISONER_SPRITE_WIDTH * nprisoners)) / (nprisoners + 1)
        for p in range(0, nprisoners):
            start_position = (self.PRISONER_SPRITE_WIDTH * p) + (gap * (p + 1)), 3
            prisoner = Prisoner(start_position)
            prisoner.add(prisoners)

        # Comienza el juego!
        pygame.time.set_timer(USEREVENT+2, 0)       # Ready screen
        pygame.time.set_timer(USEREVENT+1, 1000)    # Game's time
        return enemies, prisoners, enemy_shoots, enemy_box

    def get_start_position_for_enemy(self, index_enemy, total_enemies):
        screen = pygame.display.get_surface()

        row_index = index_enemy / self.MAX_ENEMIES_PER_ROW
        offset_y = self.ENEMY_ROW_TOP_ADDITIONAL_MARGIN + \
                   self.ENEMY_ROW_GAP * (row_index + 1) + (row_index * self.ENEMY_SPRITE_HEIGHT)

        total_rows = ((total_enemies - 1) / self.MAX_ENEMIES_PER_ROW) + 1
        # Si es la primera cmabia el tema
        if total_rows == 1:
            total_enemies_row = total_enemies
        # Tambien si es la ultima
        elif (row_index + 1) == total_rows:
            total_enemies_row = total_enemies - ((total_rows - 1) * self.MAX_ENEMIES_PER_ROW)
        else:
            total_enemies_row = self.MAX_ENEMIES_PER_ROW

        if total_rows > 1:
            while index_enemy >= self.MAX_ENEMIES_PER_ROW:
                index_enemy -= (self.MAX_ENEMIES_PER_ROW)

        gap = (screen.get_width() - (self.ENEMY_SPRITE_WIDTH * total_enemies_row)) / (total_enemies_row + 1)
        offset_x = (self.ENEMY_SPRITE_WIDTH * index_enemy) + (gap * (index_enemy + 1))
        return offset_x, offset_y

    def render_transparent_box(self, margin):
        screen = pygame.display.get_surface()
        s = pygame.Surface((screen.get_width() - (2 * margin), screen.get_height() - (2 * margin)), pygame.SRCALPHA)
        s.fill((50, 50, 50, 128))
        self.get_background().blit(s, (margin, margin))

    def render_title(self, text, level, fontcolor=(32, 32, 32)):
        if level == 1:
            fontsize = 70
            margintop = 50
        elif level == 2:
            fontsize = 50
            margintop = 110
        if pygame.font:
            screen = pygame.display.get_surface()
            font = pygame.font.Font(None, fontsize)
            text = font.render(text, 1, fontcolor)
            self.get_background().blit(text, ((screen.get_width() - text.get_width()) / 2, margintop))

    def render_menu_basics(self):
        self.refresh_background()
        self.render_transparent_box(20)
        self.render_title("PythonMan Vs PHP Invaders", 1, (255, 255, 100))

    def show_main_stage(self):
        self.render_menu_basics()
        options = pygame.sprite.RenderPlain()
        xcoord = 120
        ycoord = 120
        menu_items = GameConfig.get_ordered_menu_items()
        for index in menu_items:
            option = self.place_button_in_screen(index, xcoord, ycoord)
            option.add(options)
            xcoord += 150
        return options

    #def place_button_in_screen(self, label, sprite_x, sprite_y, xcoord, ycoord):
    def place_button_in_screen(self, index, xcoord, ycoord):
        option = Option(index, xcoord, ycoord)
        font = pygame.font.Font(None, 40)
        text = font.render(index.capitalize(), 1, (250, 250, 250))
        self.background.blit(text, (xcoord + 5, ycoord + 64))
        return option

    def get_current_stage(self):
        return self.stage

    def refresh_background(self):
        wdata = GameConfig.get_wallpaper(self.stage)
        backgrounds = pygame.image.load("backgrounds.data")
        (x, y) = wdata[1]
        (width, height) = wdata[2]

        rect = pygame.Rect((x, y, width, height))
        self.background = pygame.Surface(rect.size)
        self.background.blit(backgrounds, (0, 0), rect)

        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 22)
        text = font.render(wdata[0], 1, (40, 40, 40))
        self.background.blit(text, (screen.get_width() - (5 + text.get_width()), 3))

    def show_stage_banner(self, score=None, stage_score=None, bonus=None):
        self.refresh_background()
        self.render_transparent_box(100)
        if pygame.font:
            font = pygame.font.Font(None, 70)
            data = "STAGE " + str(self.stage)
            text = font.render(data, 1, (255, 255, 100))
            self.background.blit(text, (300, 160))
            if self.stage > 1:
                font = pygame.font.Font(None, 40)
                position_y = 190
                if bonus is not None:
                    if 'time' in bonus:
                        data = "Bonus Time " + str(bonus['time'])
                        text = font.render(data, 1, self.subtitle_font_color)
                        position_y += 30
                        self.background.blit(text, (300, position_y))
                    if 'invictus' in bonus:
                        data = "Bonus Invictus " + str(bonus['invictus'])
                        text = font.render(data, 1, self.subtitle_font_color)
                        position_y += 30
                        self.background.blit(text, (300, position_y))
                    if 'prisoners' in bonus:
                        data = "Bonus Prisoners " + str(bonus['prisoners'])
                        text = font.render(data, 1, self.subtitle_font_color)
                        position_y += 30
                        self.background.blit(text, (300, position_y))
                if stage_score is not None:
                    data = "Stage Score " + str(stage_score)
                    text = font.render(data, 1, self.subtitle_font_color)
                    position_y += 30
                    self.background.blit(text, (300, position_y))
                if score is not None:
                    data = "Total Score " + str(score)
                    text = font.render(data, 1, self.subtitle_font_color)
                    position_y += 30
                    self.background.blit(text, (300, position_y))

    def show_pause_banner(self):
        self.refresh_background()
        self.render_transparent_box(100)
        if pygame.font:
            font = pygame.font.Font(None, 70)
            data = "PAUSE"
            text = font.render(data, 1, (255, 255, 100))
            self.background.blit(text, (320, 260))

    def show_gameover_banner(self, score, stage):
        self.refresh_background()
        self.render_transparent_box(100)
        if pygame.font:
            font = pygame.font.Font(None, 70)
            data = "GAME OVER"
            text = font.render(data, 1, (255, 255, 100))
            self.background.blit(text, (250, 200))

            font = pygame.font.Font(None, 40)
            data = "Stage " + str(stage)
            text = font.render(data, 1, self.subtitle_font_color)
            self.background.blit(text, (250, 270))

            data = "Total Score " + str(score)
            text = font.render(data, 1, self.subtitle_font_color)
            self.background.blit(text, (250, 300))

            data = "Press HOME for main menu"
            text = font.render(data, 1, self.subtitle_font_color)
            self.background.blit(text, (220, 400))

    def show_victory_banner(self, score):
        if pygame.font:
            font = pygame.font.Font(None, 70)
            data = "GLORIOUS VICTORY!"
            text = font.render(data, 1, (32, 32, 32))
            self.background.blit(text, (150, 220))

            font = pygame.font.Font(None, 40)
            data = "total score " + str(score)
            text = font.render(data, 1, self.subtitle_font_color)
            self.background.blit(text, (150, 300))

            data = "Press HOME for main menu"
            text = font.render(data, 1, self.subtitle_font_color)
            self.background.blit(text, (150, 400))

    def show_about_stage(self):
        self.render_menu_basics()
        self.render_title("About this game", 2)
        options = pygame.sprite.RenderPlain()
        option = self.place_button_in_screen("back", 60, 120)
        option.add(options)

        y_offset = 160
        font = pygame.font.Font(None, 32)
        text = GameConfig.get_text('about')
        for line in text:
            data = font.render(line, 1, self.subtitle_font_color)
            self.background.blit(data, (155, y_offset))
            y_offset += 30

        return options

    def show_rules_stage(self):
        self.render_menu_basics()
        self.render_title("Rules", 2)
        options = pygame.sprite.RenderPlain()
        option = self.place_button_in_screen("back", 60, 120)
        option.add(options)

        fontsubtitle = pygame.font.Font(None, 40)
        #Enemigos
        text = fontsubtitle.render("Enemies", 1, (180, 180, 180))
        self.background.blit(text, (180, 150))
        font = pygame.font.Font(None, 32)
        y_offset = 200
        index = 0
        for e in GameConfig.get_enemy_types():
            image = Enemy.get_image(index)
            self.background.blit(image, (180, y_offset))
            data = font.render(str(e['score']) + " pts", 1, self.subtitle_font_color)
            self.background.blit(data, (250, y_offset + 20))
            y_offset += 80
            index += 1

        #Friends
        text = fontsubtitle.render("Friends", 1, (180, 180, 180))
        self.background.blit(text, (500, 150))
        image = Prisoner.get_image()
        self.background.blit(image, (500, 200))
        text = GameConfig.get_text('prisoner')
        y_offset = 200
        for line in text:
            data = font.render(line, 1, self.subtitle_font_color)
            self.background.blit(data, (550, y_offset))
            y_offset += 30

        image = SpecialItem.get_image('extra_life')
        self.background.blit(image, (430, 420))
        data = font.render("Extra life", 1, self.subtitle_font_color)
        self.background.blit(data, (470, 420))

        image = SpecialItem.get_image('invincible')
        self.background.blit(image, (570, 420))
        data = font.render("Invincible", 1, self.subtitle_font_color)
        self.background.blit(data, (610, 420))

        image = SpecialItem.get_image('super_shoot')
        self.background.blit(image, (500, 470))
        data = font.render("Super shoot", 1, self.subtitle_font_color)
        self.background.blit(data, (540, 470))

        return options