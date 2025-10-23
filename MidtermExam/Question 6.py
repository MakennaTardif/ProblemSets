# Question 6 (not finished)
from psychopy import visual, event, core

win = visual.Window(size=(800,600), color="white", units="pix") # Here I am creating a window that does not use the full screen
                                                                # I also set the window to be white, and to use pixels

# I need to first create a fixation cross 
fixation = visual.TextStim(win, text="+", color="black", height=30, pos=(0, 0)) # It is a text stim since I do not have a presaved image
                                                                                # associated with the window created above
                                                                                # text is a + (so a fixation)
                                                                                # height is 30 pixels
                                                                                # positioned in the middle of the screen

# I also need to create the "GO" stim (i.e., also a text stim)
trial_text = visual.TextStim(win, text="GO", color="black", height=40, pos=(0, 0)) # Similar specifications to the fixation

# I next need to create a clock
rt_clock = core.Clock() # I will need a clock so I can record RT data

# How many trials will there be?
Num_Trials = 1  # I personally want more than 1, but you asked for 1

# Where are the results of this trial going to be appended to?
results = [] # Added this to collect the result(s)

instructions_text = (    # I know you did not ask for this, but I added it anyway since I also did for my visual search problem set
    "Welcome to the experiment!\n\n\n"
    "There will be 1 trial for you to complete.\n\n"
    "Your job is to press SPACE as quickly as you can after the fixation cross disappears from the screen.\n\n"
    "Press SPACE to start the experiment.\n\n"
    "Or ESC to leave the experiment."
)

instructions = visual.TextStim(win, text=instructions_text, color="black", height=20, wrapWidth=900, pos=(0, 0))  

instructions.draw()  # Draws the instructions created above 
win.flip()           # Flips the instructions onto the screen for the subject to see

keys = event.waitKeys(keyList=["space", "escape"])  # Wait for a subject response 
                                                    # They are able to click the space bar or escape 

if "escape" in keys:   # If escape is pressed, close and quit experiment
    win.close()
    core.quit()

for trials in range(Num_Trials): # This is where I got stuck for some reason
                                 # I got the fixation to appear....but could not get further (one timing issue but also, I am missing something_
    
    fixation.draw()      # Draw the fixation at the beginning of each trial
    win.flip()           # Flip the fixtaion onto the screen for the subject to see 
    core.wait(1.0)       # Leave it on the screen for 1 second (as asked) (could be longer if you wanted, but i'd argue only 500ms)
 
 #####-----missing something here -------####   
 
    trial_text.draw()    # Now I want to draw my trial text ("GO")
    rt_clock.reset()     # Reset the clock to collect RT data
    win.flip             # Flip text onto the screen for the subject to see

    response = event.waitKeys(keyList=["space", "escape"])  # Need to wait for a response (again can click space or escape)
                              
    if "escape" in response:   # So, if ESC is pressed → close the window and quit experiment 
        win.close()
        core.quit()
