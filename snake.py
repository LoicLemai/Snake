from tkinter import *
import random


#constant 
GAME_WIDTH = 1400
GAME_HEIGHT = 800
BACKGROUND_COLOR = "#000000"
DEFAULT_SIZE = 3 
GAME_SPEED = 75
MENU_SPEED = 200
SPACE_SIZE = 50 
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
MENU_BACKGROUND_COLOR = "white"
state = "menu"

class Snake:


    def __init__(self):
        self.bodySize = DEFAULT_SIZE
        self.coordinates = []
        self.squares = []
        for i in range(0, DEFAULT_SIZE):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR , tag = "snake")
            self.squares.append(square)
    

class Food :
    
    def __init__(self) :
        x = random.randint(0,(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE
        self.coordinates = [x,y] 

        canvas.create_oval(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")

def next_turn(snake, food):

    if state == "running": 
        x, y  = snake.coordinates[0]
        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE



        snake.coordinates.insert(0, (x,y))

        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")

        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:

            global score

            score += 1  

            label.config(text = "Score:{}".format(score))

            canvas.delete("food")

            food = Food()

        else :

            del snake.coordinates[-1]

            canvas.delete(snake.squares[-1])
            
            del snake.squares[-1]

        if check_collisions(snake):
            game_over()
        else:
            
            window.after(GAME_SPEED, next_turn, snake, food)

    # elif state == "menu": 
    #     if direction == "up" and cursor_pos < 0:
    #         cursor_pos -= 1 
    #     elif direction == "down" and cursor_pos < 0:
    #         cursor_pos += 1 
        
        
            



def change_direction(newDirection):

    global direction

    
    if newDirection == "left" and direction!="right":
        direction=newDirection
    elif newDirection == "right" and direction!="left":
        direction=newDirection
    elif newDirection == "up" and direction!="down":
        direction=newDirection
    elif newDirection == "down" and direction!="up":
        direction=newDirection

    

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            game_over()
            return True
    
    return False 
    

    


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")


def menu_selector(item):
    pass





#WINDOW 

window = Tk()
window.title("Snake")
window.resizable(False, False)
score = 0
direction = "down"
cursor_pos = 0 

canvas = Canvas(window, bg=MENU_BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

canvas.pack()
window.update()


# if state == "menu" :   
#     print("wwaaa")
#     canvas.delete(ALL)
#     canvas.create_rectangle(10, 10, BUTTON_WIDTH , BUTTON_HEIGHT, fill="#F5D0A9", tags="menuStart")
#     canvas.create_text(5+BUTTON_WIDTH/2, 5+BUTTON_HEIGHT/2, font=10 ,text = "START")
    

#     if cursor_pos == 0 : 
#         canvas.itemconfigure("menuStart", outline="black", width = 5)  

#     window.bind("<Return>", lambda event: startGame())
   




canvas.delete(ALL)
label = Label(window, text="Score : {}".format(score), font=("consolas", 40))
label.pack()
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
    


canvas.delete(ALL)
# canvas.create_rectangle(10, 10, BUTTON_WIDTH , BUTTON_HEIGHT, fill="#F5D0A9", tags="menuStart")
# canvas.create_text(5+BUTTON_WIDTH/2, 5+BUTTON_HEIGHT/2, font=10 ,text = "START")


    
    





window.mainloop()