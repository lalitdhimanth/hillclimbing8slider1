import pygame
import random
import time
from Sprite import *
from Setting import *
from hillclimb import *

class Game:
    def __init__(self):
        pygame.init()
        self.scene = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.isshuffle = False
        self.choice1 = ""
        self.start_game = False
        self.start_timer = False
        self.timetaken = 0
        self.solution = 0
        self.count = 0
        self.currstate=0
        self.stepcount = 0
        
    def create_game(self):
        matrixpuzzle = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        matrixpuzzle[-1][-1] = 0
        return matrixpuzzle

    def shuffle(self):
        movespossible = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        movespossible.append("right")
                    if tile.left():
                        movespossible.append("left")
                    if tile.up():
                        movespossible.append("up")
                    if tile.down():
                        movespossible.append("down")
                    break
            if len(movespossible) > 0:
                break

        if self.choice1 == "right":
            movespossible.remove("left") if "left" in movespossible else movespossible
        elif self.choice1 == "left":
            movespossible.remove("right") if "right" in movespossible else movespossible
        elif self.choice1 == "up":
            movespossible.remove("down") if "down" in movespossible else movespossible
        elif self.choice1 == "down":
            movespossible.remove("up") if "up" in movespossible else movespossible

        choice = random.choice(movespossible)
        self.choice1 = choice
        if choice == "right":
            self.puzzle[row][col], self.puzzle[row][col + 1] = self.puzzle[row][col + 1], \
                                                                       self.puzzle[row][col]
        elif choice == "left":
            self.puzzle[row][col], self.puzzle[row][col - 1] = self.puzzle[row][col - 1], \
                                                                       self.puzzle[row][col]
        elif choice == "up":
            self.puzzle[row][col], self.puzzle[row - 1][col] = self.puzzle[row - 1][col], \
                                                                       self.puzzle[row][col]
        elif choice == "down":
            self.puzzle[row][col], self.puzzle[row + 1][col] = self.puzzle[row + 1][col], \
                                                                       self.puzzle[row][col]

    def draw2(self):
        self.tiles = []
        for row, x in enumerate(self.puzzle):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))
        if self.solution == 1:
            #Tile(self, 600,20, str(self.stepcount) ,self.stepcount)
            
            self.buttns.append(Button(660,20,200,50, str(self.stepcount),WHITE,BLACK))
            self.stepcount+=1

    def createnewgame(self):
        self.all = pygame.sprite.Group()
        self.puzzle = self.create_game()
        self.solutionpuzzle = self.create_game()
        self.timetaken = 0
        self.start_timer = False
        self.start_game = False
        self.solutionstates=[]
        self.buttns = []
        self.buttns.append(Button(600, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttns.append(Button(550,20,100,50, "Steps",WHITE,BLACK))
        self.buttns.append(Button(600, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttns.append(Button(600,290,200,50,"Hint",WHITE,BLACK))
        self.buttns.append(Button(600,370,200,50,"Solution",WHITE,BLACK))
        self.draw2()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.puzzle == self.solutionpuzzle:
                self.start_game = False
                

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.timetaken = time.time() - self.timer

        if self.isshuffle:
            self.shuffle()
            self.draw2()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.isshuffle = False
                self.start_game = True
                self.start_timer = True
        
        self.all.update()

    def draw_matrixpuzzle(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.scene, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.scene, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.scene.fill(BGCOLOR)
        self.all.draw(self.scene)
        self.draw_matrixpuzzle()
        for b in self.buttns:
            b.draw(self.scene)
        
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if  self.isshuffle:
                    if self.puzzle == self.solutionpuzzle:
                        pygame.quit()
                        quit(0)
                if self.solution == 0:
                    x, y = pygame.mouse.get_pos()
                    for row, i in enumerate(self.tiles):
                        for col, j in enumerate(i):
                            if j.click(x, y):
                                if j.right() and self.puzzle[row][col + 1] == 0:
                                    self.puzzle[row][col], self.puzzle[row][col + 1] = self.puzzle[row][col + 1], self.puzzle[row][col]

                                if j.left() and self.puzzle[row][col - 1] == 0:
                                    self.puzzle[row][col], self.puzzle[row][col - 1] = self.puzzle[row][col - 1], self.puzzle[row][col]

                                if j.up() and self.puzzle[row - 1][col] == 0:
                                    self.puzzle[row][col], self.puzzle[row - 1][col] = self.puzzle[row - 1][col], self.puzzle[row][col]

                                if j.down() and self.puzzle[row + 1][col] == 0:
                                    self.puzzle[row][col], self.puzzle[row + 1][col] = self.puzzle[row + 1][col], self.puzzle[row][col]
                                if self.puzzle == self.solutionpuzzle:
                                    self.buttns.append(Button(500,230,400,50,"Solved" , RED ,BLACK))
                                else:
                                    self.buttns.append(Button(500,230,400,50,"UNSOLVED" , WHITE ,BLACK))
                                self.draw2()

                    for button in self.buttns:
                        if button.click(x, y):
                            if button.text == "Shuffle":
                                self.shuffle_time = 0
                                self.isshuffle = True
                            if button.text == "Reset":
                                self.createnewgame()
                            if button.text=="Hint":
                                self.tempmatrix = hill_climbing(self.puzzle)
                                print("Hint founs")
                                for i in self.tempmatrix:
                                    if i == self.puzzle :
                                        continue
                                    else:
                                        self.puzzle = i 
                                        break
                                self.draw2()
                                # self.tiles_matrixpuzzle=self.tiles_matrixpuzzle_completed
                            if button.text=="Solution":
                                self.solutionstates = hill_climbing(self.puzzle)
                                for i in self.solutionstates:
                                    print(i)
                                self.solution = 1
                                print("SOLUTION FOUND")
                else:
                    if len(self.solutionstates) == 0 and self.count == 0 :
                        self.count+=1
                        
                    elif self.count==1:
                        pygame.quit()
                        quit(0)

                    for i in self.solutionstates:
                        self.puzzle = i
                        self.solutionstates.pop(0)
                        break
                    if self.puzzle == self.solutionpuzzle:
                                    self.buttns.append(Button(500,230,400,50,"Solved" , RED ,BLACK))
                    else:
                        self.buttns.append(Button(500,230,400,50,"UNSOLVED" , WHITE ,BLACK))
                    self.draw2()

game = Game()
while True:
    game.createnewgame()
    game.run()