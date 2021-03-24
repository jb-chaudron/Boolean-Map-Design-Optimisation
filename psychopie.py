from psychopy import core, visual, event, data, gui
import csv, random, time

win = visual.Window([800,400], color = (256,256,256),fullscr = True, monitor="testMonitor")
forme = [(0.5,0.5),(0,0.5),(0,0),(0.5,0)]
image = visual.ShapeStim(win,verticesPix = forme, fillColor = [0,100,200])
image.draw()
win.flip()
core.wait(2.0)