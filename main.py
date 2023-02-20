from tkinter import *
from tkinter import simpledialog
import json
import matplotlib.pyplot as plt
import random

GAME_WIDTH = 1400
GAME_HEIGHT = 800
BACKGROUND_COLOR = "#000000"
DEFAULT_SIZE = 3 
SPEED = 50
SPACE_SIZE = 50 
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100 
MENU_SPEED = 100
BUTTON_DETACHMENT = BUTTON_HEIGHT/2 + 25 

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

        def getSnake(): 
            return self 
    
class Food :
    def __init__(self) :
        x = random.randint(0,(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0,(GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE
        self.coordinates = [x,y]
        canvas.create_oval(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")
        def getFood(): 
            return self 

#Game loop 

def next_turn(snake, food):

    global state
    if state == "running" : 
        canvas.config(background="black")
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
            window.after(SPEED, next_turn, snake, food)

#Menu loop (graphics and interaction)

def menu_next_turn():    
    global menuSelector, state , direction
    if state == "menu":
        canvas.delete(ALL)
        canvas.config(background="white")
        if -1 < menuSelector < 2  : 
            if direction == "up" and menuSelector-1 != -1 :
                menuSelector -= 1 
            elif direction == "down" and menuSelector+1 != 2:
                print("oui")
                menuSelector += 1 
        
        startButton = canvas.create_rectangle((GAME_WIDTH/2)-(BUTTON_WIDTH/2), ((GAME_HEIGHT/2)-(BUTTON_HEIGHT/2))-BUTTON_DETACHMENT,(GAME_WIDTH/2)+(BUTTON_WIDTH/2), ((GAME_HEIGHT/2)+(BUTTON_HEIGHT/2))-BUTTON_DETACHMENT, tags="startButton")
        highscoreButton = canvas.create_rectangle((GAME_WIDTH/2)-(BUTTON_WIDTH/2), ((GAME_HEIGHT/2)-(BUTTON_HEIGHT/2))+BUTTON_DETACHMENT,(GAME_WIDTH/2)+(BUTTON_WIDTH/2), ((GAME_HEIGHT/2)+(BUTTON_HEIGHT/2))+BUTTON_DETACHMENT, tags = "highscoreButton")
        text = canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2-BUTTON_DETACHMENT, text="START", fill="black", font=("Arial", 20))
        text = canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2+BUTTON_DETACHMENT, text="HIGHSCORE", fill="black", font=("Arial", 20))

        match menuSelector:
            case 0:
                canvas.itemconfigure("startButton", outline="black",width=5)
                canvas.itemconfigure("highscoreButton", outline="black", width=1)
                unbindScore()
                bindStart()
                
            case 1:
                canvas.itemconfigure("startButton", outline="black",width=1)
                canvas.itemconfigure("highscoreButton", outline="black", width=5)
                unbindStart()
                bindScore()
              

        direction = ""
        window.after(MENU_SPEED, menu_next_turn)


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
    
    
def start_game(): 
    global state, snake, food, direction, score, label

    if state != "running" :
        canvas.delete(ALL)
        score = 0
        label.config(text="Score : {}".format(score))
        label.pack()
        direction = "down"
        print("enter")
        state = "running"
        snake = Snake()
        food = Food()
        next_turn(snake, food)
            


def game_over():
    global state, menuSelector
    saveScore()
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")
    state = "menu"
    menuSelector = 0 
    menu_next_turn()
    print("game over")


#Create a pop up where the player put his name
#function called each time the player start a new game 

def enterName():
    global name 
    name = simpledialog.askstring("Name", "Please enter your name")
    if name is not None: 
        start_game()


#Save the score in json file (save.json)

def saveScore():
    global name, score
    with open("save.json", "r") as f: 
        data = json.load(f)

    data.append({
        'name' : name,
        'score' : score
    })
    
    with open("save.json", "w") as f :
        json.dump(data,f)

#show the score using matplotlib 

def showSave():

    names = []
    scores = []

    with open("save.json", "r") as f: 
        save = json.load(f)

    for index, record in enumerate(save):
        names.append(record['name'])
        scores.append(record['score'])
    
    plt.bar(names,scores)
    plt.xlabel("Player")
    plt.ylabel("Score")
    plt.title("All time Score")
    plt.show()


#Prevent the return button to be bind twice 

def unbindStart():
    global startBind
    if startBind == True:
        print("unbind")
        window.unbind("<Return>")
        startBind = False

def bindStart():
    global startBind
    if startBind == False:
        print("bind")
        window.bind("<Return>", lambda event: enterName())
        startBind = True
  
def bindScore():
    global scoreBind
    if scoreBind == False:
        print("bind")
        window.bind("<Return>", lambda event: showSave())
        scoreBind = True

def unbindScore():
    global scoreBind
    if scoreBind == True:
        print("unbind")
        window.unbind("<Return>")
        scoreBind = False
        

#VARIABLE
scoreBind = False
startBind = False
score = 0 
retry = 0
menuSelector = 0
state = "menu"

#WINDOW 

window = Tk()
window.title("Snake")
window.resizable(False, False)
direction = "down"
label = Label(window, text="Score : {}".format(score), font=("consolas", 40))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update()

menu_next_turn()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))


window.mainloop()