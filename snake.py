import pygame, sys, random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.destroy_block = False

        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load(
            "Graphics/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            "Graphics/body_horizontal.png"
        ).convert_alpha()

        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (
                        previous_block.x == -1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == -1
                    ):
                        screen.blit(self.body_tl, block_rect)
                    elif (
                        previous_block.x == -1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == -1
                    ):
                        screen.blit(self.body_bl, block_rect)
                    elif (
                        previous_block.x == 1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == 1
                    ):
                        screen.blit(self.body_tr, block_rect)
                    elif (
                        previous_block.x == 1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == 1
                    ):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        elif self.destroy_block == True:
            body_copy = self.body[:]
            body_copy.pop()
            self.body = body_copy[:]
            self.destroy_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def remove_block(self):
        if len(self.body) > 3:
            self.destroy_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size,
        )
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(question_space, cell_number + question_space - 1)
        self.pos = Vector2(self.x, self.y)


questions = [
    {
        "question": "What is 8 × (12 - 4)/2?",
        "options": {"a": "32", "b": "40", "c": "48", "d": "56"},
        "correct_answer": "48",
    },
    {
        "question": "Evaluate 15 - 4/2 + (3 × 2).",
        "options": {"a": "14", "b": "15", "c": "16", "d": "17"},
        "correct_answer": "16",
    },
    {
        "question": "What is (12 × 5 - 7)/3?",
        "options": {"a": "17", "b": "19", "c": "21", "d": "23"},
        "correct_answer": "17",
    },
    {
        "question": "Calculate (2^3 × 5 - 3)/4.",
        "options": {"a": "4", "b": "5", "c": "6", "d": "7"},
        "correct_answer": "5",
    },
    {
        "question": "Determine (21 + 6 × 3)/9.",
        "options": {"a": "6", "b": "7", "c": "8", "d": "9"},
        "correct_answer": "7",
    },
    {
        "question": "What is 3 × (4 - 2)^2?",
        "options": {"a": "6", "b": "9", "c": "12", "d": "15"},
        "correct_answer": "12",
    },
    {
        "question": "Calculate (25 - 6 × 2)/(4 + 1).",
        "options": {"a": "1", "b": "2", "c": "3", "d": "4"},
        "correct_answer": "1",
    },
    {
        "question": "Find the value of 8 × ((15/3) - 2).",
        "options": {"a": "8", "b": "12", "c": "16", "d": "20"},
        "correct_answer": "12",
    },
    {
        "question": "What is (10 + (2 × 4)^2)/6?",
        "options": {"a": "6", "b": "8", "c": "10", "d": "12"},
        "correct_answer": "12",
    },
]


class OPTION:
    def __init__(self, value, x, y):
        self.value = value
        self.pos = Vector2(x, y)


class QUESTION:
    def __init__(self):
        self.randomize()

    def draw_question(self):
        question_rect = pygame.Rect(
            0, 0, cell_number * cell_size, question_space * cell_size
        )
        pygame.draw.rect(screen, (255, 255, 255), question_rect)
        question_surface = game_font.render(self.question, True, (56, 74, 12))
        score_rect = question_surface.get_rect(
            center=(
                int(cell_size * (cell_number / 2)),
                int(cell_size * (question_space / 2)),
            )
        )
        screen.blit(question_surface, score_rect)

    def draw_options(self):
        for option in self.options:
            option_surface = game_font.render(option.value, True, (56, 74, 12))
            answer_rect = pygame.Rect(
                int(option.pos.x * cell_size),
                int(option.pos.y * cell_size),
                cell_size,
                cell_size,
            )
            screen.blit(option_surface, answer_rect)

    def randomize(self):
        random_question = random.choice(questions)
      #   random_question = questions[0]
        self.question = random_question["question"]
        print(self.question)
        self.correct_answer = random_question["correct_answer"]
        self.options = []
        used_pos = {(0,0)}
        for option in random_question["options"].values():
            x = y = 0
            while (x,y) in used_pos:
               x = random.randint(0, cell_number - 1)
               y = random.randint(question_space, cell_number + question_space - 1)
            print(x,y)
            used_pos.add((x,y))
            self.options.append(OPTION(option, x, y))


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.question = QUESTION()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        # self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.question.draw_question()
        self.question.draw_options()
        self.draw_score()

    def check_collision(self):
        for option in self.question.options:
            if option.pos == self.snake.body[0]:
                if option.value == self.question.correct_answer:
                    self.snake.add_block()
                else:
                    self.snake.remove_block()
                self.question.randomize()
                self.snake.play_crunch_sound()

            # for block in self.snake.body[1:]:
            # 		# if block == self.question.pos:
            # 		# 		self.question.randomize()

    def check_fail(self):
        # print(self.snake.body[0].x,self.snake.body[0].y)
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not question_space <= self.snake.body[0].y < cell_number + question_space
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(question_space, cell_number + question_space):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 6,
            apple_rect.height,
        )

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 15
question_space = 2


screen = pygame.display.set_mode(
    (cell_number * cell_size, (cell_number + question_space) * cell_size)
)
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 40)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
