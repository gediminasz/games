import pygame


class Joystick:
    def __init__(self):
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            print('Failed to detect a joystick.')
            self.joystick = None

    @property
    def frets(self):
        if not self.joystick:
            return [False] * 5
        return map(self.joystick.get_button, (1, 2, 3, 0, 4))

    @property
    def is_strumming(self):
        return self.joystick.get_hat(0)[1] if self.joystick else False
