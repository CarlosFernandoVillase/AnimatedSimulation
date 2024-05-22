# Make sure to use the command pip install simpy
# And after running the simulation it will ask you if you want to see the data of every single day, type "y" for yes and "n" for no
# And also at the end just enter the number of the day you wish to see animated

import numpy as np
import matplotlib.pyplot as plt
import simpy
import random
from enum import Enum
import os
from time import sleep
import pygame

pygame.init()

clock = pygame.time.Clock()
clock.tick()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Object: # Each gear that spawns
    def __init__(self, object_img, objectX, objectY):
        self.object_img = object_img
        self.objectX = objectX
        self.objectY = objectY

    def update(self, speed):
        self.objectX += speed

class OBJECTS: # This one creates and updates each gear as time goes on
    def __init__(self):
        self.Objects = []
    
    def createObject(self,objectX, objectY, state):
        object_img = pygame.image.load("gear.png")
        objectBroken_img = pygame.image.load("gearBroken.png")
        image = object_img
        if state == "done":
            image = object_img
        elif state == "fail":
            image = objectBroken_img
        object = Object(image, objectX, objectY)
        self.Objects.append(object)

    def renderObjects(self):
        for object in self.Objects:
            object.update(4)
            screen.blit(object.object_img,(object.objectX,object.objectY))

class Day(object): #Each day in the simulation
    def __init__(self, dayNumber, TOP) -> None:
        self.dayNumber = dayNumber
        self.TOP = TOP
        self.done = 0
        self.fail = 0
        self.OLP = 0
        self.x = []

    def count(self,products):
        W=0
        L=0
        for product in products:
          if product == "done":
            W+=1
          elif product == "fail":
            L+=1
        return W, L

    def simulate_day(self, OLP):
        self.x =random.choices(["done", "fail"], weights = [.97, .03], k = round(random.normalvariate(100, 5)))
        self.done, self.fail = self.count(self.x)
        self.OLP = OLP - self.done
        if self.OLP < 0:
          self.OLP = 0
        return self.OLP

    def calculateTotal(self,doneTot,failTot):
        doneTot += self.done
        failTot += self.fail
        return doneTot,failTot

    def getPerformance(self):
        return self.done, self.fail, self.dayNumber

    def display_status(self):
        print(f"Day {self.dayNumber}:")
        print(f"Total orders planned: {self.TOP}")
        print(f"Produced items: {self.done}")
        print(f"Failed items: {self.fail}")
        print(f"Orders left planned: {self.OLP}")
        print() 
    
    def display_day_x(self):
        i = 0
        timer = 0
        run = True
        while i < (len(self.x)-1) and run == True:
            screen.fill((60,60,60))

            timer+=1
            
            if timer > 60:
                Objects.createObject(objectX, objectY, self.x[i])
                timer = 0
                i +=1

            Objects.renderObjects()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(30)

            pygame.display.update()


class Factory(object): # The factory
    def __init__(self, TOP) -> None:
        self.days = []
        self.TOP = TOP


    def simulate_business(self):
        OLP = TOP
        i = 1
        while OLP > 0:
            day = Day(i, self.TOP)
            OLP = day.simulate_day(OLP)
            self.days.append(day)
            i += 1
        print("======================")
        print("Simulation Successful")
        print(f"All Orders have been completed in {i-1} days")
        print()

    def calculateTotal(self,doneTot,failTot):
        for day in self.days:
            doneTot,failTot = day.calculateTotal(doneTot,failTot)
        return doneTot,failTot

    def getPerformance(self,y1,y2,x):
        for day in self.days:
            Ry1,Ry2,Rx = day.getPerformance()
            y1.append(Ry1)
            y2.append(Ry2)
            x.append(Rx)
        return y1,y2,x
        

    def display_status(self):
        for day in self.days:
            day.display_status()
            sleep(1)

    def display_certain_day(self,day):
        self.days[day-1].display_day_x()
       


Objects = OBJECTS()

# Initial variables
TOP = 5000 # Total orders planned
array= []
doneTot=0
failTot=0

objectX=50
objectY=240

# Run the factory simulation
factory = Factory(TOP)
factory.simulate_business()

# Graphs
doneTotT,failTotT = factory.calculateTotal(doneTot,failTot)

def percentage(x,y):
  return round(((x)/(x+y))*100,2)

y1 = []
y2 = []
x = []

R1, R2, RX = factory.getPerformance(y1,y2,x)
  
# plot lines 
plt.style.use('dark_background')

plt.plot(RX, R1, color=(.1,.9,.1) ,label = "Success") 
plt.plot(RX, R2, color=(1,.2,.2),label = "Errors") 
plt.legend() 
plt.xlabel("Day")
plt.ylabel("Product Amount")
plt.title("Simulation Production Performance")
plt.show()
print()


plt.pie([doneTotT,failTotT], labels = [f"Succesful\n{percentage(doneTotT,failTotT)}%",f"Failed\n{percentage(failTotT,doneTotT)}%"], colors=[(.1,.9,.1),(1,.2,.2)])
plt.title("Simulation Error Rate")

plt.show() 
print()

print("Do you wish to see the data of every single day in the simulation? (y/n)")
inp = input()
if inp == "y":
  #Display the data from every day
  factory.display_status()
elif inp == "n":
  print("Understood")

# The animated simulation of a specified day
print("Please enter the number of the day you wish to see the visual representation of")
Snum = input()
num = int(Snum)
factory.display_certain_day(num)
