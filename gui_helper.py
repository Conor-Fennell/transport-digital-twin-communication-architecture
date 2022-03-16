import turtle

def createLoopGui():
   
    pen = turtle.Turtle()
    pen.color("WHITE")
    pen.width(3)
    pen.hideturtle()
    pen.penup()
    pen.goto(-400, 400)
    pen.fd(360)
    pen.rt(90)
    pen.pendown()

    pen.fd(1080)

    pen.penup()
    pen.rt(90)
    pen.fd(360)
    pen.rt(90)
    pen.pendown()

    pen.fd(1080)

    pen.penup()
    pen.rt(90)
    pen.goto(0, 400)
    pen.fd(360)
    pen.rt(90)
    pen.pendown()

    pen.fd(1080)

    pen.penup()
    pen.rt(90)
    pen.fd(360)
    pen.rt(90)
    pen.pendown()

    pen.fd(1080)

    #NORTHBOUND
    Nb_l1 =turtle.Turtle()
    Nb_l1.shape("circle")
    Nb_l1.color("blue")
    Nb_l1.fillcolor("black")
    Nb_l1.penup()
    Nb_l1.goto(-360, 65)
    Nb_l1.pendown()
    Nb_l1.shapesize(3)

    Nb_l2 =turtle.Turtle()
    Nb_l2.shape("circle")
    Nb_l2.color("blue")
    Nb_l2.fillcolor("black")
    Nb_l2.penup()
    Nb_l2.goto(-270, 65)
    Nb_l2.pendown()
    Nb_l2.shapesize(3)

    Nb_l3 =turtle.Turtle()
    Nb_l3.shape("circle")
    Nb_l3.color("blue")
    Nb_l3.fillcolor("black")
    Nb_l3.penup()
    Nb_l3.goto(-180, 65)
    Nb_l3.pendown()
    Nb_l3.shapesize(3)

    Nb_l4 =turtle.Turtle()
    Nb_l4.shape("circle")
    Nb_l4.color("blue")
    Nb_l4.fillcolor("black")
    Nb_l4.penup()
    Nb_l4.goto(-90, 65)
    Nb_l4.pendown()
    Nb_l4.shapesize(3) 


    #SOUTHBOUND
    Sb_l1 =turtle.Turtle()
    Sb_l1.shape("circle")
    Sb_l1.color("blue")
    Sb_l1.fillcolor("black")
    Sb_l1.penup()
    Sb_l1.goto(315, 65)
    Sb_l1.pendown()
    Sb_l1.shapesize(3)

    Sb_l2 =turtle.Turtle()
    Sb_l2.shape("circle")
    Sb_l2.color("blue")
    Sb_l2.fillcolor("black")
    Sb_l2.penup()
    Sb_l2.goto(225, 65)
    Sb_l2.pendown()
    Sb_l2.shapesize(3)

    Sb_l3 =turtle.Turtle()
    Sb_l3.shape("circle")
    Sb_l3.color("blue")
    Sb_l3.fillcolor("black")
    Sb_l3.penup()
    Sb_l3.goto(135, 65)
    Sb_l3.pendown()
    Sb_l3.shapesize(3)

    Sb_l4 =turtle.Turtle()
    Sb_l4.shape("circle")
    Sb_l4.color("blue")
    Sb_l4.fillcolor("black")
    Sb_l4.penup()
    Sb_l4.goto(45, 65)
    Sb_l4.pendown()
    Sb_l4.shapesize(3) 

    return Nb_l1, Nb_l2, Nb_l3, Nb_l4, Sb_l1, Sb_l2, Sb_l3, Sb_l4
    

def lightOn(light):
    light.fillcolor("blue")
    
def lightsOff(lights):
    for light in lights:
        light.fillcolor("black")