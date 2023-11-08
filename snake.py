import pygame
import random

pygame.init()


class Snake_game:
    def __init__(self, window, window_height, window_width) -> None:
        self.window_height: int = window_height
        self.window_width: int = window_width
        self.window = window
        pygame.display.set_caption("Snake game")

        self.game_over: bool = False
        self.direction_of_travel = None

        # score and level
        self.score: int = 0
        self.level: int = 1

        # Colors, fonts etc
        self.white: tuple = (255, 255, 255)
        self.black: tuple = (0, 0, 0)
        self.green: tuple = (173, 245, 47)
        self.gray: tuple = (80, 80, 80)
        self.light_gray: tuple = (211, 211, 211)
        self.font = pygame.font.Font(None, 20)

    # method to display score in the screen
    def display_score(self) -> None:
        score_info: str = f"Score: {self.score} | Level: {self.level}"
        text_width, text_height = self.font.size(score_info)
        text = self.font.render(score_info, True, self.white)
        self.window.blit(text, ((self.window_width / 2) - (text_width / 2), 10))

    # Function to display text in center of the screen
    def display_centered_text(self, text, color, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.window_width // 2, y))
        self.window.blit(text_surface, text_rect)

    # Screen to show when game is over
    def game_over_screen(self):
        while self.game_over:
            self.window.fill(self.black)  # Set the screen to green
            self.display_centered_text(
                text="Game over", color=self.white, y=self.window_height / 2
            )
            self.display_centered_text(
                f"Your score: {self.score}",
                color=self.white,
                y=(self.window_height / 2) + 20,
            )

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = False  # Allow quitting the game

    def play_game(self) -> None:
        # Initial position of snake and length
        x1: int = round(self.window_width / 2)
        y1: int = round(self.window_height / 2)
        length_of_snake: int = 1
        snake_body: list = []

        # Initial change of snake position by px on each tick
        x1_change: int = 0
        y1_change: int = 0

        # Food position - must be exactly divisible by 10 because the snake moves 10px at a time
        x2: int = random.randint(2, (self.window_width - 10) / 10) * 10
        y2: int = random.randint(2, (self.window_height - 10) / 10) * 10

        while not self.game_over:
            for event in pygame.event.get():
                # Check for arrow keys pressed
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_LEFT
                        # Sanke can only move to the direction it is facing
                        and self.direction_of_travel != 1073741903
                    ):
                        x1_change = -10
                        y1_change = 0
                        self.direction_of_travel = event.key

                    elif (
                        event.key == pygame.K_RIGHT
                        and self.direction_of_travel != 1073741904
                    ):
                        x1_change = 10
                        y1_change = 0
                        self.direction_of_travel = event.key
                    elif (
                        event.key == pygame.K_UP
                        and self.direction_of_travel != 1073741905
                    ):
                        x1_change = 0
                        y1_change = -10
                        self.direction_of_travel = event.key

                    elif (
                        event.key == pygame.K_DOWN
                        and self.direction_of_travel != 1073741906
                    ):
                        x1_change = 0
                        y1_change = 10
                        self.direction_of_travel = event.key

            # Current position of snake
            x1 = x1 + x1_change
            y1 = y1 + y1_change

            # Eating food
            if x1 == x2 and y1 == y2:
                length_of_snake += 1
                self.score += 100
                x2 = random.randint(0, (self.window_width - 10) / 10) * 10
                y2 = random.randint(0, (self.window_height - 10) / 10) * 10
                self.level = (self.score // 1000) + 1

            # Game over when snake hits wall
            if x1 >= self.window_width or x1 < 2 or y1 >= self.window_height or y1 < 2:
                self.game_over = True

            # Snake head
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)

            snake_body.append(snake_head)

            # delete old cordinates of snake body
            if len(snake_body) > length_of_snake:
                del snake_body[0]

            # Game over when snake hits its body
            if snake_head in snake_body[:-1]:
                self.game_over = True

            self.window.fill(color=self.black)

            # Border effect on the window itself
            pygame.draw.rect(
                surface=self.window,
                color=self.gray,
                rect=[1, 1, self.window_width - 2, self.window_height - 2],
            )
            pygame.draw.rect(
                surface=self.window,
                color=self.black,
                rect=[3, 3, self.window_width - 6, self.window_height - 6],
            )

            # Drawing initial food item
            pygame.draw.rect(
                surface=self.window, color=self.green, rect=[x2, y2, 10, 10]
            )

            # Drawing the snake
            for segment in snake_body:
                # drawing twice to get border effect
                pygame.draw.rect(
                    surface=self.window,
                    color=self.gray,
                    rect=[segment[0], segment[1], 10, 10],
                )
                pygame.draw.rect(
                    surface=self.window,
                    color=self.white,
                    rect=[segment[0], segment[1], 10 - 1, 10 - 1],
                )

            # Display score and level
            self.display_score()
            pygame.display.update()

            # Game speed
            clock = pygame.time.Clock()
            clock.tick((self.level // 100) + 10)

        self.game_over_screen()


if __name__ == "__main__":
    # Defining window size and window itself
    window_height: int = 600
    window_width: int = 800
    window = pygame.display.set_mode((window_width, window_height))

    # Initializing and starting game
    game = Snake_game(window, window_height, window_width)
    game.play_game()
