import pygame
from pygame.locals import *
from player import Player
from stagegenerator import StageGenerator
from gamestatus import GameStatus
from gameconfig import GameConfig


class GameEngine():

    def __init__(self, modes=None):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        #Modes
        self.cheater_mode = False
        if modes is not None and 'cheater' in modes and modes['cheater'] is True:
            self.cheater_mode = True

        # Stage Generator
        self.stage_generator = StageGenerator()
        # Game Status
        self.game_status = GameStatus()
        pygame.display.set_caption('PHP Invaders')
        pygame.mouse.set_visible(0)
        self.stage_quantity = GameConfig.get_stage_quantity()

        self.clock = pygame.time.Clock()
        self.enemy_box = None

        #Screens
        self.screen_type_data = {"mainmenu": 1, "playing": 2, "pause": 3, "waiting4stage": 4, "gameover": 5}
        self.screen_type = None

        #Sprites
        self.sprites = {
            'friendly_fire': pygame.sprite.RenderPlain(),
            'enemy_fire': pygame.sprite.RenderPlain(),
            'enemies': pygame.sprite.RenderPlain(),
            'friends': pygame.sprite.RenderPlain(),
            'menu_options': pygame.sprite.RenderPlain(),
            'special_items': pygame.sprite.RenderPlain(),
            'prisoners': pygame.sprite.RenderPlain(),
            'others': pygame.sprite.RenderPlain(),
        }
        self.player = Player()
        self.player.add(self.sprites['friends'])

        #Others
        self.show_main_stage()
        self.screen.blit(self.stage_generator.get_background(), (0, 0))
        pygame.display.flip()

    def is_current_screen(self, key):
        return self.screen_type_data[key] == self.screen_type

    def set_current_screen(self, key):
        self.screen_type = self.screen_type_data[key]

    def clock_tick(self):
        self.clock.tick(60)

    def reset_from_gameover(self):
        self.sprites['enemies'].empty()
        self.sprites['enemy_fire'].empty()
        self.sprites['prisoners'].empty()
        self.player.reset()
        self.game_status.reset()
        self.stage_generator.reset()

    def show_main_stage(self):
        self.screen_type = self.screen_type_data["mainmenu"]
        self.sprites['menu_options'] = self.stage_generator.show_main_stage()

    #Game Status Bar
    def refresh_status_bar(self):
        screen = pygame.display.get_surface()
        offset_y = screen.get_height()-20
        pygame.draw.rect(self.stage_generator.get_background(), (0, 0, 0), pygame.Rect(0, screen.get_height() - 25, screen.get_width(), 25), 0);
        if pygame.font:
            font = pygame.font.Font(None, 20)
            fontcolor = (250, 250, 250)
            status_data = [
                ("ver. " + GameConfig.get_version() + " by Ismael Liceras", 600),
                ("STAGE " + str(self.game_status.get_stage()), 10),
                ("LIVES " + str(self.game_status.get_lives()), 110),
                ("TIME " + str(self.game_status.get_time()), 210),
                ("SCORE " + str(self.game_status.get_score()), 310)
            ]
            for data_piece in status_data:
                text = font.render(data_piece[0], 1, fontcolor)
                self.stage_generator.get_background().blit(text, (data_piece[1], offset_y))

    def handle_lifecycle_events(self, event):
        if event.type == QUIT:
            return -1
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return -1
        elif event.type == KEYDOWN and event.key == K_HOME:
            self.reset_from_gameover()
            self.show_main_stage()
        elif event.type == KEYDOWN and event.key == K_PAUSE:
            if self.is_current_screen("pause"):
                self.set_current_screen("playing")
                self.stage_generator.refresh_background()
            elif self.is_current_screen("playing"):
                self.set_current_screen("pause")
                self.stage_generator.show_pause_banner()

    def handle_playerops_events(self, event):
        if event.type == KEYDOWN and not self.is_current_screen('pause'):
            if event.key == K_LEFT:
                self.player.go_left()
            elif event.key == K_RIGHT:
                self.player.go_right()
            elif event.key == K_SPACE and not self.is_current_screen('gameover'):
                shoot = self.player.do_shoot()
                shoot.add(self.sprites['friendly_fire'])
        elif event.type == KEYUP and \
                ((event.key == K_LEFT and self.player.get_direction() == 'left') or
                (event.key == K_RIGHT and self.player.get_direction() == 'right')):
            self.player.stop_flying()

    def handle_timer_events(self, event):
        #Game's time
        if event.type == USEREVENT + 1:
            if self.is_current_screen("playing"):
                time = self.game_status.run_1_sec()
                if time == 0:
                    self.go_to_gameover()

        #Ready's screen
        elif event.type == USEREVENT + 2:
            self.sprites['enemies'], self.sprites['prisoners'],\
                self.sprites['enemy_fire'], self.enemy_box = self.stage_generator.start_next_stage()
            pygame.time.set_timer(USEREVENT+1, 1000)
            self.set_current_screen('playing')
            self.stage_generator.refresh_background()

    def handle_cheat_mode_events(self, event):
        if event.type == KEYDOWN and self.is_current_screen('playing'):
            if event.key == K_n:
                print "Next Stage!"
                for dead_enemy in self.sprites['enemies']:
                    dead_enemy.add(self.sprites['others'])
                    dead_enemy.remove(self.sprites['enemies'])
                    dead_enemy.kill_enemy()

    def handle_events(self):
        for event in pygame.event.get():
            # Exit and pause
            if self.handle_lifecycle_events(event) == -1:
                return -1
            # Player's ops
            self.handle_playerops_events(event)
            # Timer's events
            self.handle_timer_events(event)
            # Cheat mode events
            if self.cheater_mode is True:
                self.handle_cheat_mode_events(event)

    def check_player2enemies_collision(self):
        collision = pygame.sprite.groupcollide(self.sprites['friendly_fire'], self.sprites['enemies'], True, False)
        if len(collision) > 0:
            key, value = collision.popitem()
            dead_enemy = value[0]
            dead_enemy.add(self.sprites['others'])
            dead_enemy.remove(self.sprites['enemies'])
            dead_enemy.kill_enemy()
            self.game_status.add_score(dead_enemy.get_score())
            special_item = dead_enemy.drop_special_item()
            if special_item is not None:
                special_item.add(self.sprites['special_items'])

    def check_enemies2player_collision(self):
        collision = pygame.sprite.groupcollide(self.sprites['enemy_fire'], self.sprites['friends'], True, False)
        if len(collision) > 0:
            if self.player.is_invincible() is not True:
                self.hit_player()

    def hit_player(self):
        if self.game_status.remove_life() == 0:
            self.go_to_gameover()
        else:
            self.player.shocked()
            self.game_status.set_stage_invictus(False)

    def check_menu_collision(self):
        collision = \
            pygame.sprite.groupcollide(self.sprites['friendly_fire'], self.sprites['menu_options'], True, True)
        if len(collision) > 0:
            key, value = collision.popitem()
            option_choosen = value[0]
            self.sprites['menu_options'].empty()
            if option_choosen.get_type_id() == "play":
                self.set_current_screen('waiting4stage')
                self.go_to_next_stage()
            elif option_choosen.get_type_id() == "about":
                self.stage_generator.refresh_background()
                self.sprites['menu_options'] = self.stage_generator.show_about_stage()
            elif option_choosen.get_type_id() == "rules":
                self.sprites['menu_options'] = self.stage_generator.show_rules_stage()
            elif option_choosen.get_type_id() == "back":
                self.stage_generator.refresh_background()
                self.sprites['menu_options'] = self.stage_generator.show_main_stage()
            elif option_choosen.get_type_id() == "exit":
                exit()

    def check_player2specialitem(self):
        collision = pygame.sprite.groupcollide(self.sprites['friends'], self.sprites['special_items'], False, True)
        if len(collision) > 0:
            #Player pilla objeto especial!
            key, value = collision.popitem()
            item = value[0]
            item.do_action(self)

    def check_player2prisoners_collision(self):
        collision = pygame.sprite.groupcollide(self.sprites['friendly_fire'], self.sprites['prisoners'], True, True)
        if len(collision) > 0:
            self.hit_player()

    def check_collisions(self):
        if self.is_current_screen('playing'):
            # Player shoots enemies
            self.check_player2enemies_collision()
            # Player shoots prisoners
            self.check_player2prisoners_collision()
            # Enemies shoot player
            self.check_enemies2player_collision()
        elif self.is_current_screen('mainmenu'):
            self.check_menu_collision()
        if self.is_current_screen('playing') or self.is_current_screen('waiting4stage'):
            self.check_player2specialitem()

    def go_to_next_stage(self, bonus=None):
        self.set_current_screen("waiting4stage")
        self.stage_generator.get_ready_to_next_stage(self.game_status.get_score(), self.game_status.get_stage_score(), bonus)
        self.game_status.reset_to_next_stage(self.stage_generator.get_current_stage())

    def check_stage_clear(self):
        if self.is_current_screen('playing') and len(self.sprites['enemies']) == 0:
            bonus = self.add_stage_bonus()
            if self.stage_generator.get_current_stage() >= self.stage_quantity:
                self.goto_to_victory()
            else:
                self.go_to_next_stage(bonus)

    def add_stage_bonus(self):
        bonus = {}
        bonus['time'] = self.game_status.add_bonus_time()
        if self.game_status.get_stage_invictus():
            bonus['invictus'] = self.game_status.add_bonus_invictus()
        if len(self.sprites['prisoners']) > 0:
            bonus['prisoners'] = self.game_status.add_bonus_prisoners(len(self.sprites['prisoners']))
        return bonus

    # GameEngine's main method
    def do_play(self):
        self.clock_tick()
        self.check_collisions()

        if self.is_current_screen('playing'):
            self.check_stage_clear()

        self.update_sprites()
        self.draw_everything()

    def draw_everything(self):
        if not self.is_current_screen('mainmenu'):
            self.refresh_status_bar()

        self.screen.blit(self.stage_generator.get_background(), (0, 0))
        self.sprites['friendly_fire'].draw(self.screen)
        self.sprites['enemy_fire'].draw(self.screen)
        self.sprites['enemies'].draw(self.screen)
        self.sprites['friends'].draw(self.screen)
        self.sprites['menu_options'].draw(self.screen)
        self.sprites['special_items'].draw(self.screen)
        self.sprites['prisoners'].draw(self.screen)
        self.sprites['others'].draw(self.screen)
        pygame.display.flip()

    def update_sprites(self):
        if not self.is_current_screen('pause'):
            self.update_enemies()
            self.sprites['friendly_fire'].update()
            self.sprites['enemy_fire'].update()
            self.sprites['enemies'].update()
            self.sprites['friends'].update()
            self.sprites['special_items'].update()
            self.sprites['prisoners'].update()
            self.sprites['others'].update()

    def update_enemies(self):
        if self.enemy_box is not None:
            self.enemy_box.update()

    def go_to_gameover(self):
        self.player.kill_player()
        self.set_current_screen("gameover")
        self.stage_generator.refresh_background()
        self.stage_generator.show_gameover_banner(self.game_status.score, self.game_status.stage)

    def goto_to_victory(self):
        self.player.make_winner()
        self.set_current_screen("gameover")
        self.stage_generator.refresh_background()
        self.stage_generator.show_victory_banner(self.game_status.score)