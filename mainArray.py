#  Copyright 2015 Vitalii Shmorgun <vcshmorgun@yandex.ru>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import bge
import random
import GameLogic
import math

scene = GameLogic.getCurrentScene()

def start():
	GameLogic.p = 0
	GameLogic.slot = 0
	GameLogic.Re = 0
	GameLogic.mainArray = [ 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7',
							'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7',
							'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7',
							'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7',
							'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7',
							'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 
							'']    
	GameLogic.M = 0
	cont = bge.logic.getCurrentController()
	own = cont.owner
	shufleBalls()

def shufleBalls():
	random.shuffle(GameLogic.mainArray) 
	for k in range(8):
		#-----------reset rower position
		towerBlock = scene.objects['t'+ str(k)] 
		rot = towerBlock.worldOrientation.to_euler()
		rot.z = 0
		towerBlock.localOrientation = rot
		#-------------------------------------
		if k < 7:
			for i in range(6):
				n = (i*7)+k
				if GameLogic.mainArray[n]:
					ball = scene.objects[GameLogic.mainArray[n]]
					pos = ball.position
					pos[2] = k * 0.4
					rot = ball.worldOrientation.to_euler()
					rot.z = i * math.pi/3
					ball.localOrientation = rot
		else:
			if GameLogic.mainArray[42]:
				ball = scene.objects[GameLogic.mainArray[42]]
				pos = ball.position
				pos[2] = -0.4
				rot = ball.worldOrientation.to_euler()
				rot.z = 0
				ball.localOrientation = rot

def relocateRow(row, mov):
	tempRow = ['','','','','','']
	for i in range(6):
		n = row + (i*7)
		if GameLogic.mainArray[n]:
			ball = scene.objects[GameLogic.mainArray[n]]
			rot = ball.worldOrientation.to_euler()
			rot.z = absRot(rot.z)
			ball.localOrientation = rot
			tempRow[GameLogic.p] = GameLogic.mainArray[n]
	for i in range(6):
		n = row + (i*7)
		GameLogic.mainArray[n] = tempRow[i]

def redawColumn(col):         
	if col == GameLogic.slot:
		if GameLogic.mainArray[42]:
			ball = scene.objects[GameLogic.mainArray[42]]
			pos = ball.position
			pos[2] = -0.4
	for i in range(7):
		n = i + col*7
		if GameLogic.mainArray[n]:
			ball = scene.objects[GameLogic.mainArray[i + col*7]]
			pos = ball.position
			pos[2] = i * 0.4
	
#----------------------------------------------------------------
def absRot(rot):
	print(GameLogic.M)
	aRot = (rot + (math.pi*2))%(math.pi*2)
	print(aRot)
	if((aRot < (math.pi/6))or(aRot > (11*math.pi/6))):
		rot = 0
		GameLogic.p = 0
# 60 deg
	elif( (aRot > (math.pi/6))and( aRot < (math.pi/2) ) ):
		rot = (math.pi/3)
		GameLogic.p = 1
# 120 deg
	elif( (aRot > (math.pi/2))and( aRot < (5*math.pi/6) ) ):
		rot = (2*math.pi/3)
		GameLogic.p = 2
# 180 deg
	elif( (aRot > (5*math.pi/6))and( aRot < (7*math.pi/6) ) ):
		rot = (math.pi)
		GameLogic.p = 3
# 240 deg
	elif( (aRot > (7*math.pi/6))and( aRot < (math.pi+math.pi/2) ) ):
		rot = (4*math.pi/3)  
		GameLogic.p = 4     
# 300 deg
	elif( (aRot > (math.pi+math.pi/2))and( aRot < (11*math.pi/6) ) ):
		rot = (5*math.pi/3)  
		GameLogic.p = 5    
	return(rot)
#----------------------------------------------------------------
def relocateLastRow():
	m = abs(GameLogic.M)
	if m > 0:
		towerBlock = scene.objects['t'+ str(m-1)] 
		rot = towerBlock.worldOrientation.to_euler()
		rot.z = absRot(rot.z)
		towerBlock.localOrientation = rot
		if m > 1:
			relocateRow(m-2,rot.z)
		elif m == 1:
			GameLogic.slot = GameLogic.p 
			if GameLogic.mainArray[42]:
				ball = scene.objects[GameLogic.mainArray[42]]
				ball.localOrientation = rot   
def main():  
	controller = bge.logic.getCurrentController()
	player = controller.owner
	bMess = player.sensors["RollMessage"]
	startMess = player.sensors["ShuffleMessage"]
	vertMess =  player.sensors["JumpToMessage"]
	mouseOutMess =  player.sensors["MouseOut"]
#If start or press on Shuffle button    
	if startMess.positive:
		start()  
		
#If press on ball for moving to empty space in column    
	if vertMess.positive:
		name = vertMess.bodies[0]
		aNum = GameLogic.mainArray.index(name)
		bb = 0
		col = aNum//7
		if aNum == 42:
			bb = 1
			col = GameLogic.slot
		e = GameLogic.mainArray.index('')
		eCol = e//7
		if e == 42:
			eCol = GameLogic.slot
			if eCol == col:
				GameLogic.mainArray[42] = GameLogic.mainArray[col * 7]
				GameLogic.mainArray[col * 7] = ''
				e = col * 7
		if col == eCol:
			if bb:
				aNum = col * 7 
			d = e
			s = -1
			if (aNum > e):
				s = 1
			while d != aNum:
				GameLogic.mainArray[d] = GameLogic.mainArray[d+s]
				GameLogic.mainArray[d+s] = ''
				d += s  
			if bb:
				GameLogic.mainArray[col * 7] = GameLogic.mainArray[42]
				GameLogic.mainArray[42] = ''
			redawColumn(col)    
	 
#If press button for rotating some row        
	if (mouseOutMess.positive):
		relocateLastRow()
	if bMess.positive:
		m = int(bMess.bodies[0])
		rotSpeed = 0
		if   m > 0:
			rotSpeed =  0.05
		elif m < 0:
			rotSpeed = -0.05
		GameLogic.M = m            
		m = abs(m)
		towerBlock = scene.objects['t'+ str(m-1)]  
		towerBlock.applyRotation((0,0,rotSpeed),True)
		if m > 1:
			for i in range(6):
				n = (m-2)+(i*7)
				if GameLogic.mainArray[n]:
					ball = scene.objects[GameLogic.mainArray[n]]
					ball.applyRotation((0,0,rotSpeed),True)
		elif m == 1:
			if GameLogic.mainArray[42]:
				ball = scene.objects[GameLogic.mainArray[42]]
				ball.applyRotation((0,0,rotSpeed),True)
	else:
		relocateLastRow()
main()
