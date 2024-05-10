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

questions = [
    {
        "question": "3 * 4 + 5",
        "options": {"a": "17", "b": "18", "c": "19", "d": "20"},
        "correct_answer": "17"
    },
    {
        "question": "10 - 2 * 3",
        "options": {"a": "4", "b": "6", "c": "8", "d": "10"},
        "correct_answer": "4"
    },
    {
        "question": "15 / 3 + 2",
        "options": {"a": "5", "b": "6", "c": "7", "d": "8"},
        "correct_answer": "7"
    },
    {
        "question": "6 * (4 - 2)",
        "options": {"a": "8", "b": "10", "c": "12", "d": "14"},
        "correct_answer": "12"
    },
    {
        "question": "20 / (5 - 2)",
        "options": {"a": "4", "b": "6", "c": "8", "d": "10"},
        "correct_answer": "10"
    }

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
            0, 0, cell_number_x * cell_size, question_space * cell_size
        )
        pygame.draw.rect(screen, (255, 255, 255), question_rect)
        question_surface = game_font.render(self.question, True, (56, 74, 12))
        score_rect = question_surface.get_rect(
            center=(
                int(cell_size * (cell_number_x / 2)),
                int(cell_size * (question_space / 2)),
            )
        )
        screen.blit(question_surface, score_rect)

    def draw_options(self):
        for option in self.options:
            print(type(option.value), "option")
            option_surface = game_font.render(str(option.value), True, (56, 74, 12))
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
        # self.question = random_question["question"]
        # print(self.question)
        self.question,options,self.correct_answer = self.generate_mcq()
        # self.correct_answer = random_question["correct_answer"]
        self.options = []
        used_pos = {(0,0)}
        for option in options:
            x = y = 0
            while (x,y) in used_pos:
               x = random.randint(0, cell_number_x - 1)
               y = random.randint(question_space, cell_number_y + question_space - 1)
            # print(x,y)
            used_pos.add((x,y))
            self.options.append(OPTION(option, x, y))

    def generate_mcq(self):
        # Generate random numbers and operators
        # num_count = random.randint(2, 5)  # Generate between 2 to 5 numbers
        num_count = 2
        nums = [random.randint(1, 10) for _ in range(num_count)]
        operators = [random.choice(['+', '-', '*']) for _ in range(num_count - 1)]
        
        # Generate the question string
        question = f"{''.join(str(num) + ' ' + op for num, op in zip(nums, operators))} {nums[-1]}"
        
        # Calculate the correct answer
        answer = nums[0]
        for num, op in zip(nums[1:], operators):
            if op == '+':
                answer += num
            elif op == '-':
                answer -= num
            elif op == '*':
                answer *= num
            elif op == '/':
                # Avoid division by zero and ensure integer division
                if num == 0:
                    num = 1
                answer /= num
        
        # Generate incorrect options
        options = []
        while len(options) < 3:
            incorrect_answer = random.randint(int(answer) - 10, int(answer) + 10)
            if incorrect_answer != answer and incorrect_answer not in options:
                options.append(incorrect_answer)
        
        # Shuffle the options
        options.append(answer)
        random.shuffle(options)
        
        return question, options, answer

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.question = QUESTION()
        self.timer = 10 

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def reset_timer(self):
        self.timer = 10

    def draw_elements(self):
        self.draw_grass()
        # self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.question.draw_question()
        self.question.draw_options()
        self.draw_score()
        self.draw_timer()

    def check_collision(self):
        for option in self.question.options:
            if option.pos == self.snake.body[0]:
                if option.value == self.question.correct_answer:
                    self.snake.add_block()
                else:
                    self.snake.remove_block()
                self.question.randomize()
                self.snake.play_crunch_sound()
                self.reset_timer()
            # for block in self.snake.body[1:]:
            # 		# if block == self.question.pos:
            # 		# 		self.question.randomize()

    def check_fail(self):
        # print(self.snake.body[0].x,self.snake.body[0].y)
        if (
            not 0 <= self.snake.body[0].x < cell_number_x
            or not question_space <= self.snake.body[0].y < cell_number_y + question_space
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        # self.question.randomize()
        # score_surface = game_font.render("GAME OVER", True, (56, 74, 12))
        # score_rect = score_surface.get_rect(center=(cell_number_x//2, cell_number_y//2))
        # screen.blit(score_surface, score_rect)
        self.reset_timer()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(question_space, cell_number_y + question_space):
            if row % 2 == 0:
                for col in range(cell_number_x):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number_x):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number_x - 60)
        score_y = int(cell_size * cell_number_y - 40)
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

    def draw_timer(self):
        ##timer color should be red 
        timer_text = game_font.render(str(self.timer), True, (255, 0, 0))
        timer_x = cell_number_x * cell_size - 60
        timer_y = 40
        timer_rect = timer_text.get_rect(center=(timer_x, timer_y))
        screen.blit(timer_text, timer_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number_x = 38
cell_number_y = 17
question_space = 2


screen = pygame.display.set_mode(
    (cell_number_x * cell_size, (cell_number_y + question_space) * cell_size)
)
# screen = pygame.display.set_mode(
#     (0,0), pygame.FULLSCREEN
# )
print("FULLSCREEN",screen.get_size())
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 40)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # Timer event occurs every second
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
        if event.type == TIMER_EVENT:
            main_game.timer -= 1
            if main_game.timer == 0:
                main_game.snake.remove_block()
                main_game.question.randomize()
                main_game.reset_timer()
    screen.fill((175, 215, 70))
    
    main_game.draw_elements()
        # Create a timer event

    pygame.display.update()
    clock.tick(60)
