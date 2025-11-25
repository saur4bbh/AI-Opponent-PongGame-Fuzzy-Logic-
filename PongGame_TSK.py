import pygame
from typing import Type
import skfuzzy as fuzz
import skfuzzy.control as fuzzcontrol

FPS = 30


class Board:
    def __init__(self, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("AIFundamentals - PongGame")

    def draw(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class Drawable:
    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface(
            [width, height], pygame.SRCALPHA, 32
        ).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 20,
        color=(255, 10, 0),
        speed: int = 3,
    ):
        super(Ball, self).__init__(x, y, radius, radius, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = speed
        self.y_speed = speed
        self.start_speed = speed
        self.start_x = x
        self.start_y = y
        self.start_color = color
        self.last_collision = 0

    def bounce_y(self):
        self.y_speed *= -1

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y_power(self):
        self.color = (
            self.color[0],
            self.color[1] + 10 if self.color[1] < 255 else self.color[1],
            self.color[2],
        )
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed *= 1.1
        self.y_speed *= 1.1
        self.bounce_y()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x_speed = self.start_speed
        self.y_speed = self.start_speed
        self.color = self.start_color
        self.bounce_y()

    def move(self, board: Board, *args):
        self.rect.x += round(self.x_speed)
        self.rect.y += round(self.y_speed)

        if self.rect.x < 0 or self.rect.x > (
            board.surface.get_width() - self.rect.width
        ):
            self.bounce_x()

        if self.rect.y < 0 or self.rect.y > (
            board.surface.get_height() - self.rect.height
        ):
            self.reset()

        timestamp = pygame.time.get_ticks()
        if timestamp - self.last_collision < FPS * 4:
            return

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.last_collision = pygame.time.get_ticks()
                if (self.rect.right < racket.rect.left + racket.rect.width // 4) or (
                    self.rect.left > racket.rect.right - racket.rect.width // 4
                ):
                    self.bounce_y_power()
                else:
                    self.bounce_y()


class Racket(Drawable):
    def __init__(
        self,
        x: int,
        y: int,
        width: int = 80,
        height: int = 20,
        color=(255, 255, 255),
        max_speed: int = 10,
    ):
        super(Racket, self).__init__(x, y, width, height, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x: int, board: Board):
        delta = x - self.rect.x
        delta = self.max_speed if delta > self.max_speed else delta
        delta = -self.max_speed if delta < -self.max_speed else delta
        delta = 0 if (self.rect.x + delta) < 0 else delta
        delta = (
            0
            if (self.rect.x + self.width + delta) > board.surface.get_width()
            else delta
        )
        self.rect.x += delta


class Player:
    def __init__(self, racket: Racket, ball: Ball, board: Board) -> None:
        self.ball = ball
        self.racket = racket
        self.board = board

    def move(self, x: int):
        self.racket.move(x, self.board)

    def move_manual(self, x: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def act(self, x_diff: int, y_diff: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass


class PongGame:
    def __init__(
        self, width: int, height: int, player1: Type[Player], player2: Type[Player]
    ):
        pygame.init()
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.ball = Ball(width // 2, height // 2)

        self.opponent_paddle = Racket(x=width // 2, y=0)
        self.oponent = player1(self.opponent_paddle, self.ball, self.board)

        self.player_paddle = Racket(x=width // 2, y=height - 20)
        self.player = player2(self.player_paddle, self.ball, self.board)

    def run(self):
        while not self.handle_events():
            self.ball.move(self.board, self.player_paddle, self.opponent_paddle)
            self.board.draw(
                self.ball,
                self.player_paddle,
                self.opponent_paddle,
            )
            self.oponent.act(
                self.oponent.racket.rect.centerx - self.ball.rect.centerx,
                self.oponent.racket.rect.centery - self.ball.rect.centery,
            )
            self.player.act(
                self.player.racket.rect.centerx - self.ball.rect.centerx,
                self.player.racket.rect.centery - self.ball.rect.centery,
            )
            self.fps_clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                return True
        keys = pygame.key.get_pressed()
        if keys[pygame.constants.K_LEFT]:
            self.player.move_manual(0)
        elif keys[pygame.constants.K_RIGHT]:
            self.player.move_manual(self.board.surface.get_width())
        return False


class NaiveOponent(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(NaiveOponent, self).__init__(racket, ball, board)

    def act(self, x_diff: int, y_diff: int):
        x_cent = self.ball.rect.centerx
        self.move(x_cent)


class HumanPlayer(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(HumanPlayer, self).__init__(racket, ball, board)

    def move_manual(self, x: int):
        self.move(x)


# ----------------------------------
# DO NOT MODIFY CODE ABOVE THIS LINE
# ----------------------------------

import numpy as np
import matplotlib.pyplot as plt

class FuzzyPlayer(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super().__init__(racket, ball, board)

        w = board.surface.get_width() / 2
        self.x_universe = np.arange(-w, w + 1)
        self.x_mf = {
            "far_left":  fuzz.trapmf(self.x_universe, [-w, -w, -250, -120]),
            "left":      fuzz.trimf(self.x_universe, [-200, -100, 0]),
            "center":    fuzz.trimf(self.x_universe, [-50, 0, 50]),
            "right":     fuzz.trimf(self.x_universe, [0, 100, 200]),
            "far_right": fuzz.trapmf(self.x_universe, [120, 250, w, w]),
        }

        h = board.surface.get_height()
        self.y_universe = np.arange(0, h + 1)
        self.y_mf = {
            "close": fuzz.trapmf(self.y_universe, [0, 0, 50, 200]),
            "mid": fuzz.trimf(self.y_universe, [100, 200, 300]),
            "far": fuzz.trapmf(self.y_universe, [200, 350, h, h]),
        }

        self.base_velocity = {
            "fast_left":  -2.8,
            "slow_left":  -1.4,
            "stop":        0,
            "slow_right":  1.4,
            "fast_right":  2.8,
        }

        self.rules = {
            ("far_left", "close"): "fast_left",
            ("left", "close"): "slow_left",
            ("center", "close"): "stop",
            ("right", "close"): "slow_right",
            ("far_right", "close"): "fast_right",

            ("far_left", "mid"): "fast_left",
            ("left", "mid"): "slow_left",
            ("center", "mid"): "stop",
            ("right", "mid"): "slow_right",
            ("far_right", "mid"): "fast_right",

            ("far_left", "far"): "fast_left",
            ("left", "far"): "slow_left",
            ("center", "far"): "stop",
            ("right", "far"): "slow_right",
            ("far_right", "far"): "fast_right",
        }

        #Visualization
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        for name, mf in self.x_mf.items():
            plt.plot(self.x_universe, mf, label=name, linewidth=2)
        plt.title("X difference fuzzy sets")
        plt.xlabel("x_diff (paddle vs ball)")
        plt.ylabel("Membership degree")
        plt.legend()

        plt.subplot(1, 2, 2)
        for name, mf in self.y_mf.items():
            plt.plot(self.y_universe, mf, label=name, linewidth=2)
        plt.title("Y difference fuzzy sets")
        plt.xlabel("y_diff (paddle vs ball)")
        plt.ylabel("Membership degree")
        plt.legend()

        plt.tight_layout()
        plt.show()

    def act(self, x_diff: int, y_diff: int):
        velocity = self.make_decision(x_diff, y_diff)
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: float, y_diff: float):

        x_memberships = {name: fuzz.interp_membership(self.x_universe, mf, -x_diff)
                         for name, mf in self.x_mf.items()}


        y_memberships = {name: fuzz.interp_membership(self.y_universe, mf, abs(y_diff))
                         for name, mf in self.y_mf.items()}

        num = den = 0

        for x_name, x_md in x_memberships.items():
            for y_name, y_md in y_memberships.items():
                activation = min(x_md, y_md)
                if activation > 0:
                    vel_label = self.rules.get((x_name, y_name), "stop")
                    v = self.base_velocity[vel_label]
                    v *= abs(self.ball.x_speed) #dynamic vel
                    
                    num += activation * v
                    den += activation

        vel = num / den
        return 0 if den == 0 else vel



if __name__ == "__main__":
    #game = PongGame(800, 400, NaiveOponent, HumanPlayer)
    game = PongGame(800, 400, NaiveOponent, FuzzyPlayer)
    game.run()