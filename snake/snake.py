import pygame
import random
import time

snake_block_size = 30
snake_color = (255,255,255)
snake_border_width = 1
snake_border_color = None
snake_init_length = 1
food_color = (255,0,0)
food_size = snake_block_size
food_inc = 1
game_width = 40*snake_block_size
game_height = 30*snake_block_size
tick_speed = 10
text_size = 30



class Food(object):
    def __init__(self):
        self.size = food_size
        self.color = food_color
        self.x = None
        self.y = None

    def randCoords(self, xmax, ymax):
        x = round(random.randrange(0, xmax-self.size) / float(self.size)) * float(self.size)
        y = round(random.randrange(0, ymax-self.size) / float(self.size)) * float(self.size)
        return x,y

    def update(self, xmax, ymax, avoid=[]):
        while True:
            coords = self.randCoords(xmax, ymax)
            if not coords in avoid:
                self.x = coords[0]
                self.y = coords[1]
                break

    def draw(self, display):
        pygame.draw.rect(display, self.color, [ self.x, self.y, self.size, self.size ])



class Snake(object):
    def __init__(self, startx, starty):
        self.snake = [ (startx, starty) for i in range(snake_init_length) ]
        self.x_change = 0
        self.y_change = 0
        self.keymap = { pygame.K_LEFT: (-1,0), pygame.K_RIGHT:(1,0), pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1) }

    def update(self, left, right, top, bottom):
        oldHead = self.snake[-1]
        newHead = (oldHead[0]+self.x_change, oldHead[1]+self.y_change)
        if self.x_change != 0 or self.y_change != 0:
            if newHead in self.snake or newHead[0]<left or newHead[0]>right-snake_block_size or newHead[1]<top or newHead[1]>bottom-snake_block_size:
                return False
            self.snake.append(newHead)
            del self.snake[0]
        return newHead

    def updateChange(self, event):
        if event.key in self.keymap:
            change = self.keymap[event.key]
            self.x_change = change[0]*snake_block_size
            self.y_change = change[1]*snake_block_size

    def draw(self, display):
        for s in self.snake:
            if snake_border_color:
                pygame.draw.rect(display, snake_border_color, [ s[0], s[1], snake_block_size, snake_block_size ])
            pygame.draw.rect(display, snake_color, [ s[0], s[1], snake_block_size-snake_border_width, snake_block_size-snake_border_width ])


class Game():
    def __init__(self, game_width=game_width, game_height=game_height, title="Snake Game", bg_color=(0,0,0), food_inc=food_inc):
        pygame.init()
        self.bg_color = bg_color
        self.display = pygame.display.set_mode((game_width, game_height))
        pygame.display.set_caption(title)
        self.snake = None
        self.food = None
        self.clock = pygame.time.Clock()
        self.width = game_width
        self.height = game_height
        self.food_inc = food_inc
        self.score = 0

    def setFood(self):
        self.food = Food()
        self.food.update(self.width, self.height)

    def setSnake(self):
        self.snake = Snake(self.width/2, self.height/2)


    def updateDisplay(self):
        self.display.fill(self.bg_color) # clear display
        if not self.snake.update(0, self.width, 0, self.height): # attempt to update snake
            print("DEAD")
            return True
        snakeHead = self.snake.snake[-1]
        if snakeHead[0] == self.food.x and snakeHead[1] == self.food.y:
            self.score += 1
            self.food.update(self.width, self.height, self.snake.snake)
            for _ in range(self.food_inc):
                self.snake.snake.insert(0, self.snake.snake[0])
        self.displayScore()
        self.snake.draw(self.display)
        self.food.draw(self.display)
        pygame.display.update()
        self.clock.tick(tick_speed)
        return False


    def displayScore(self):
        font = pygame.font.SysFont(None, text_size)
        mesg = font.render("Score: {}".format(self.score), True, (0,0,255, 0.2))
        mesg_h, mesg_w = mesg.get_size()
        self.display.blit(mesg, [ self.width/2-mesg_h/2, 0 ])

    def displayMessage(self, msg="", font_size=text_size, font_style=None, color=(0,255,0)):
        font = pygame.font.SysFont(font_style, font_size)
        mesg = font.render(msg, True, color)
        mesg_h, mesg_w = mesg.get_size()
        self.display.blit(mesg, [ self.width/2-mesg_h/2, self.height/2-mesg_w/2 ])

    def run(self, tick_speed=10):
        self.setSnake()
        self.setFood()
        game_over = False
        game_close = False
        count = 3

        while not game_close:
            while game_over == True:
                self.displayMessage("You Lost! | Score: {} | Press Q-Quit or C-Play Again".format(self.score))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        game_over = False
                        game_close = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                            self.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_close = True
                if event.type == pygame.KEYDOWN:
                    self.snake.updateChange(event)
            game_over = self.updateDisplay()

        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.setSnake()
    game.setFood()
    game.run()
