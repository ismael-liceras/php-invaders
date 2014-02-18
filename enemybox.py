import pygame


class EnemyBox():
    def __init__(self, pos, move):
        self.current_pos = self.old_pos = pos
        self.move = move
        self.area = pygame.display.get_surface().get_rect()

    def get_current_pos(self):
        return self.current_pos

    def get_old_pos(self):
        return self.old_pos

    def get_offset(self):
        x = self.current_pos.left - self.old_pos.left
        y = self.current_pos.top - self.old_pos.top
        return x, y

    def get_move(self):
        return self.move

    def update(self):
        new_pos = self.current_pos.move((self.move, 0))
        if self.current_pos.left < self.area.left or \
           self.current_pos.right > self.area.right:
            self.move = -self.move
            new_pos = self.current_pos.move((self.move, 0))
        self.current_pos = new_pos