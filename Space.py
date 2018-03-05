import turtle
import os
import random
import math

#Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Invaders")
screen.bgpic("space_invaders_background.gif")

#Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")
turtle.register_shape("invader2.gif")

#Create border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Draw the score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font = ("Arial", 14, "normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#######################

#Choose number of enemies
number_of_enemies = 5
#Create empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:

    enemy.color("red")
    oh = random.randint(0,1)
    if oh == 0:
        enemy.shape("invader2.gif")
    else:
        enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

#Create player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.setposition(player.xcor(), player.ycor())
bullet.hideturtle()

bulletspeed = 20

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Moving the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if (bulletstate == "ready"):
        os.system("afplay laser.wav&")
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y + 10)
        bullet.showturtle()
        bulletstate = "fire"

def isCollision(t1, t2, dist):
    return (math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))) < dist



#Create keybord bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#Main game loop
while True:

    #Move the enemy
    #Create the enemy
    for enemy in enemies:

        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        #Move enemies when they hit the sides
        if (enemy.xcor() > 280 or enemy.xcor() < -280):
            for e in enemies:
                enemyspeed *= -1
                y = e.ycor()
                y -= 40
                e.sety(y)

        #Check for collision between bullet and enemy
        if isCollision(bullet, enemy, 15):
            os.system("afplay explosion.wav&")
            score += 20
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font = ("Arial", 14, "normal"))
            score_pen.hideturtle()
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            #Reset enemy position
            i = random.randint(-200, 200)
            j = random.randint(100, 250)
            enemy.setposition(x, y)
            enemy.setposition(i, j)

        #Check for collision between player and enemy/enemy's bullet
        if isCollision(enemy,player, 20):
            print("Game Over")
            enemy.hideturtle()
            enemy.setposition(-200, 250)
            player.hideturtle()
            break

    #Move the bullet
    y = bullet.ycor()
    y += bulletspeed
    bullet.sety(y)

    #Change state of bullet if margin is hit
    if (y > 280):
        bulletstate = "ready"

delay = raw_input("Press enter to finish.")
