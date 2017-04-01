#!/usr/bin/env python
import os

with open('settings') as f:
	lines = f.readlines()

for s in lines:
	if s[0] == 'w':
		w = (str.split(s)[2])
	if s[0] == 'h':
		h = (str.split(s)[2])
#print(w,h)

conmmand = "blenderplayer" +  " -w " + w + " " + h + "/home/vit/ProjectLTP/blenderLTP/MiniGames/BabylonTower/tube.blend "
os.system(conmmand)
