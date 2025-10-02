#Creating a simple experiment 

from psychopy import visual, core  #Importing a psychopy library and specific modules 
win = visual.Window([400,400])   #Need to create a window to draw to (i.e., assign name, window size)
message = visual.TextStim(win, text='hello') #Draw a stimulus to the back buffer (assign label, type, and window)
message.autoDraw = True    #If autodraw == true (it will automatically draw every frame)
win.flip()         #Flip the stimulus to the screen (i.e., stimulus does not apppear until the buffer is "flipped"
core.wait(2.0)     #Delay the next events from happening (i.e., wait for 2 seconds)
message.text = 'world'  #Change the properties of existing stimulus 
win.flip()
core.wait(2.0) 

#Making a more elaborate experiment 

#Step 1: Import the necessarily libraries 
from psychopy import visual, event, core, data 

#Step 2: Create a window
win = visual.Window([1024,768], fullscr=False, units='pix')

#Step 3a: Create (but do not draw) a stimulus:
    #initialise some stimuli
fixation = visual.Circle(win, size = 5)   #size=5 pixels tall because we set units to pixels
    lineColor = 'white', fillColor = 'lightGrey')

#Step 3b: Create a second stimulus
probe = visual.GratingStim(win, size = 80, 
    pos = [300, 0],
    tex = None, mask = 'gauss',
    color = 'green')

#Step 3c: Create a third stimulus
cue = visual.ShapeStim(win,
    vertices = [[-30,-20], [-30,20], [30,0]],
    lineColor = 'red', fillColor = 'salmon')
    
#Step 4: Define some attributes for the stimuli (i.e., dictionary of keys)
info = {} # a dictionary 
info['fixTime'] = 0.5 #this is in seconds (i.e., same with the two below)
info['cueTime'] = 0.2
info['probeTime'] = 0.2

#Step 5a: Create a single trial
  # run one trial
fixtation.autoDraw = True  #draw (stay on until you turn it off - set to false if want it to go away)
win.flip()      #flip
core.wait(info['fixTime']) #wait

cue.draw()
win.flip()
core.wait(info['cueTime'])

fixation.draw()
probe.draw()
win.flip()
core.wait(info['probeTime']

#Step 5b: Run mutliple trials
for trial in range(5):     #Loops through it 5 times (i.e., 5 trials)
    fixtation.autoDraw = True  
    win.flip()      
    core.wait(info['fixTime']) 

    cue.draw()
    win.flip()
    core.wait(info['cueTime'])

    fixation.draw()
    probe.draw()
    win.flip()
    core.wait(info['probeTime']

#Challenge: Series of the 5 trials, that will have a series of valid or invalid trials
import random #importing the random library

probe = visual.GratingStim(win, size = 80, 
    pos = [300, 0],
    tex = None, mask = 'gauss',
    color = 'green')
    
cue = visual.ShapeStim(win,
    vertices = [[-30,-20], [-30,20], [30,0]],
    lineColor = 'red', fillColor = 'salmon')

side = [1,2]
orient = [1,2]

for trial in range(5):     
    
    random.shuffle(side)
    print("side:" +str(side[0]))
    random.shiffle
    print("orient:" +str(orient[0]))
    
    fixtation.draw()  
    win.flip()      
    core.wait(info['fixTime']) 
    
    if orient[0] == 1
        cue.ori = 0
    else:
        cue.ori = 180

    cue.draw()
    win.flip()
    core.wait(info['cueTime'])
    
    if side[0] == 1
        probe.pos = [30,0]
    else:
        probe.pos = [-30,0]

    fixation.draw()
    probe.draw()
    win.flip()
    core.wait(info['probeTime']
    
#Step 6a: Create a clock
respClock = core.Clock()

#Step 6b: Reset the clock when presenting stimulus
fixation.draw()
probe.draw()
win.flip() 
#comment out core.wait at the end of the loop (i.e., no longer waiting)
respClock.reset()

win.flip()  #clear screen

            #wait for response
            
keys = event.waitKeys(keyList = ['left','right','escape'])   #key options (i.e., this is a list of specific keys)
resp = keys[0]    #take first response (i.e., only want the first value = 0)
rt = respClock.getTime()     #calculate the reaction time (i.e., current time of response clock after it reset)

#Step 6c: Check for response accuracy (i.e., calculating accuracy)

if (resp == 'left' and side[0] == 2) or resp == 'right' and side[0] ==1):
    corr = 1
else:
    corr = 0
    
#Step 6d: Save the responses (i.e., track and log)    #do this within your loop

#Open file:
  fileID = open(filename, "w")   #w=write, x=open, a=append
#Write to file
  fileID.write('format', vars)   #Format (s=string, i = int, f = floating point) ('/n/ new line)
#Close file
   fileID.close()
