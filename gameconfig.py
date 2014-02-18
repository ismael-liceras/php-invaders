class GameConfig():

    version = 'pm.1.0'

    # MAX 28 enemies = 4 rows
    # (type, num)
    enemies = [
        [(1, 7), (4, 1)],
        [(2, 7), (3, 1)],
    ]

    #num
    prisoners = [
        1,
        1,
    ]

    # (type, num)
    items = [
        [('extra_life', 2), ('super_shoot', 2), ('invincible', 2)],
        [('extra_life', 2), ('super_shoot', 2), ('invincible', 2)],
    ]

    # type, velocity
    move = [
        2,
        3,
    ]

    enemy_types = [
        {'score': 10, "image": [(548, 84), (64, 64)], "shoot_timer": 200},     # Eclipse
        {'score': 20, "image": [(469, 9), (64, 64)], "shoot_timer": 100},      # Web
        {'score': 50, "image": [(468, 84), (64, 64)], "shoot_timer": 80},      # PHP
        {'score': 100, "image": [(549, 9), (64, 64)], "shoot_timer": 50}       # Drupal
    ]

    menu_items = {
        'play': [(9, 12), (64, 64)],
        'rules': [(98, 10), (64, 64)],
        'about': [(5, 86), (64, 64)],
        'exit': [(90, 86), (64, 64)],
        'back': [(686, 13), (64, 64)],
    }

    menu_order = [
        'play', 'rules', 'about', 'exit'
    ]

    player = {
        'normal': [(309, 84), (64, 64)],
        'anger': [(237, 6), (64, 64)],
        'victory': [(385, 84), (64, 64)],
        'crying': [(238, 84), (64, 64)],
        'shocked': [(380, 7), (64, 64)],
        'money': [(308, 6), (64, 64)]
    }

    special_items = {
        'extra_life': [(680, 129), (32, 32)],
        'super_shoot': [(182, 114), (32, 32)],
        'invincible': [(182, 71), (32, 32)]
    }

    others = {
        'prisoner': [(182, 17), (32, 32)],
        'super_shoot': [(627, 108), (54, 16)],
        'shoot': [(647, 88), (13, 12)],
        'fire': [(619, 11), (64, 64)],
        'enemy_shoot': [(647, 133), (16, 16)]
    }

    wallpapers = [
        ['Ciudad de las Artes y las Ciencias (Valencia)', (0, 0), (800, 600)],
        ['1', (800, 0), (800, 600)],
        ['2', (1600, 0), (800, 600)],
        ['3', (2400, 0), (800, 600)],
        ['4', (3200, 0), (800, 600)],
        ['5', (4000, 0), (800, 600)],
        ['6', (4800, 0), (800, 600)],

        ['7', (0, 600), (800, 600)],
        ['8', (800, 600), (800, 600)],
        ['9', (1600, 600), (800, 600)],
        ['10', (2400, 600), (800, 600)],
        ['11', (3200, 600), (800, 600)],
        ['12', (4000,  600), (800, 600)],
        ['13', (4800, 600), (800, 600)],

        ['14', (0, 1200), (800, 600)],
        ['15', (800, 1200), (800, 600)],
        ['16', (1600, 1200), (800, 600)],
        ['17', (2400, 1200), (800, 600)],
        ['18', (3200, 1200), (800, 600)],
        ['19', (4000, 1200), (800, 600)],
        ['20', (4800, 1200), (800, 600)],
    ]

    text = {
        'about': [
            "This game has been completely developed",
            "by Ismael Liceras, and represents the",
            "cruise of a software ingenier to quit being",
            "considered only as PHP Developer, and who is",
            "trying to find a place on the Python world.",
            "Its development took one week, it's my first",
            "videogame based on Pygame library",
            "and really enjoyed every single minute I spent",
            "on it.",
            "Please feel free to contact me at my email",
            "address: ismael.liceras@gmail.com",
            "Thanks for playing :-)"
        ],
        'prisoner': [
            "This is a prisoner...",
            "shoot him and you ",
            "will pay for it ",
            "with a life!",
            "Save him and ",
            "you will get",
            "a bonus :-)"
        ],

    }

    @staticmethod
    def get_enemies(stage):
        return GameConfig.enemies[(stage - 1)]

    @staticmethod
    def get_move(stage):
        return GameConfig.move[(stage - 1)]

    @staticmethod
    def get_items(stage):
        return GameConfig.items[(stage - 1)]

    @staticmethod
    def get_prisoners(stage):
        return GameConfig.prisoners[(stage - 1)]

    @staticmethod
    def get_stage_quantity():
        return len(GameConfig.enemies)

    @staticmethod
    def get_enemy_types():
        return GameConfig.enemy_types

    @staticmethod
    def get_enemy_type(etype):
        return GameConfig.enemy_types[etype]

    @staticmethod
    def get_menu_items(index=None):
        if index is None:
            return GameConfig.menu_items
        else:
            return GameConfig.menu_items[index]

    @staticmethod
    def get_ordered_menu_items():
        return GameConfig.menu_order

    @staticmethod
    def get_wallpaper(index):
        return GameConfig.wallpapers[index]

    @staticmethod
    def get_player(index):
        return GameConfig.player[index]

    @staticmethod
    def get_others(index):
        return GameConfig.others[index]

    @staticmethod
    def get_special_items(index):
        return GameConfig.special_items[index]

    @staticmethod
    def get_text(index):
        return GameConfig.text[index]

    @staticmethod
    def get_version():
        return GameConfig.version