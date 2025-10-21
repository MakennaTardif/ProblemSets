# First I am creating a very simple visual search experiment 
   # This experiment finds a T (target shape) among L's (distractor shapes)
   # 50% of trials contain the target T (i.e., target present trials) , while the other 50% do not (i.e., target absent trials)
   # Press "1" if the target is present, and press "0" if the target is absent.

# First I need to import the required libraries 
from psychopy import visual, event, core  # visual = drawing windows and stimuli (https://www.psychopy.org/api/visual/index.html)
                                          # core = timing/quit (https://www.psychopy.org/api/core.html)
                                          # event = keyboard presses (https://www.psychopy.org/api/event.html)

import random                             # random = randomizing trials/stim positions (I will need to do this at some point)

# Now I should create a window (i.e., the main display that stim will draw to)
   # units="pix" (simple & matches what we used in class)
   # color="white" (so the T.png's white background blends in smoothly with the experiment background)
     # If I did not change this, the background of the experiment and image would not have blended at all
   # fullscr=True is good here because then I do not need to pick a size (i.e., uses the computers full screen)
   # https://www.psychopy.org/api/visual/window.html (used this site here)
win = visual.Window(fullscr=True, color="white", units="pix") 

# Next I need to define my stimuli I will be displaying later on
   # I can make reusable ImageStim objects, then I could just change their position each time
   # https://www.psychopy.org/api/visual/imagestim.html
T_image = visual.ImageStim(win, image="T.png", size=(50, 50)) # 50 by 50 pixels (took some time to get the sizing to how I wanted it)
L_image = visual.ImageStim(win, image="L.png", size=(50, 50)) # same sizing here (do not want the target and distractors to be different sizes)

# Next I would like to create a fixation cross (since we were not given a .png file for one)
fixation = visual.TextStim(
    win,
    text="+",               # The plus sign is the fixation symbol
    color="black",          # Black color so it is visible on white background
    height=50,              # The stim size (in pixels) (kept approximately the same height in pixels as the other stim) (https://www.psychopy.org/api/visual/textstim.html_
    pos=(0, 0)              # I want this centered on the screen every time
)
# Next I should likely include an instruction screen to tell subjects what the task is/what to do
  # When I create a TextStim, nothing shows yet — it’s just *ready* to draw later on
  # I have to: Create the stim, draw it (queue it to draw), and then flip the window to show it
  # Then after flipping, I will use the event.waitKeys() to pause and wait until the subject presses a specific key

instructions_text = (           # Here I just wanted to create basic instructions for the task that the subject would eventually see
    "Welcome to the visual search experiment!\n\n\n"
    "There will be 10 trials for you to complete.\n\n"
    "On each trial, you will see 9 letters on the screen.\n\n"
    "Your task is to decide whether there is a letter 'T' amongst the 'L's.\n\n"
    "Press 1 if the 'T' is PRESENT.\n\n"
    "Press 0 if the 'T' is ABSENT.\n\n"
    "Press SPACE to start the experiment, or ESC to exit."
)

instructions = visual.TextStim(    
    win,                     # Defining the window I created above
    text=instructions_text,  # Text instrictions contains many '\n' newlines, linebreaks
    color="black",           # I need black text on white background (in order to see it)
    height=25,               # The text size in pixels (28 pixels in this case)
    wrapWidth=900,           # This wraps long lines nicely
    pos=(0, 0),              # This means the text is centered on the screen when it is flipped
)

instructions.draw()  # Draw the instructions (i.e., this queues it to be flipped)
win.flip()           # flip it onto the screen for the subject to see 
keys = event.waitKeys(keyList=["space", "escape"])  # This pauses the script and waits for the participant to press a key.
                                                    # Only the SPACE and ESCAPE key will be valid
if "escape" in keys:
    win.close()    # These two lines closethe window and stops/quits the experiment if the "escape" key is pressed
    core.quit()
    
# Next I need some basic settings (i.e., simple variables I can change in order to alter how the task will behave)
Num_Trials = 10         # This is the total number of total trials to run
Set_Size = 9            # This is how many items I want to appear on each trial
Key_Present = '1'       # This is the button to press if a T is present
Key_Absent  = '0'       # This is the button to press if a T is absent 

# I should likely define (x,y) coordinates of where I want the letters to appear (these are fixed as of now)
coordinates = [                             # These should be a grid format (this took me forever to get this how I wanted it)
    (-300, 200), (0, 200), (300, 200),      # Top row 
    (-300, 0),   (0, 0),   (300, 0),        # Middle row
    (-300, -200), (0, -200), (300, -200)    # Bottom row
]

# Now I should define how many trials have a target present and how many trials have a target absent (Creating a trial list)
trial_types = [1]*5 + [0]*5   # I specified above that 1 = target present, 0 = target absent 
                              # This line is just saying that 5 trials will have a target and 5 will not (total 10 trials)
                              # Follows the 50/50 rule suggested (i.e., 50% of trials target present, 50% absent)
                              
random.shuffle(trial_types)   # Here I randomized the order of present/absent trials (i.e., so it is not a predictable order)
                                  # https://docs.python.org/3/library/random.html (used this site to choose a random method)

# Next I need to create the main trial loop
   # It will repeat the same “show items → get a response” routine 10 times (Num_Trials)
for trial_idx in range(Num_Trials):
    # 'trial_idx' is just the placeholder for each trial (0, 1, 2, …,8).
         # In other words, this tells you which trial you’re on (e.g., Trial 1 of 9)
    # Each time this loop runs, a new display of letters will appear.
    
     # STEP 1: I need to show the fixation cross before each trial
        # The fixation cross will be displayed at the center of the screen for 1 second.
        # This helps participants center their eyes before the trial begins
    fixation.draw()       # Prepare to show fixation
    win.flip()            # Show it on screen
    core.wait(1)          # Keep it visible for 1 second (1000 ms)

    # STEP 2: I need to figure out if this trial has a T or not.
       # The list called trial_types contains the 1s and 0s.
       # Again, 1 = target-present trial (there will be a T), and 0 = target-absent trial (there will be only Ls)
       # trial_types must have exactly Num_Trials entries
    present = trial_types[trial_idx]

    # STEP 3: Now, if this trial includes a T (i.e., a 1), randomly choose which coordinate position it appears in.
       # random.randrange(Set_Size) gives a random number between 0 and Set_Size - 1
           # This number will match one of the coordinate slots in my list (e.g., 0..8 if Set_Size = 9)
       # If this is a target-absent trial, I set it to None here (so no T would be drawn to the screen)
    target_position = random.randrange(Set_Size) if present else None
              # https://docs.python.org/3/library/random.html (used this same site to pick the randrange method because set size is a given range)

    # STEP 4: Now I need to draw one letter (T or L) for each of the 9 coordinates on the screen.
       # I need to loop through every coordinate in my list
       # If this position matches the randomly chosen target slot → draw a T; otherwise → draw an L.
    for pos_idx in range(Set_Size):
        # 'pos_idx' Goes through each coordinate and draws one letter there
            # In other words, which position on the screen I am drawing to (e.g., top-left, center, bottom-right)
        if present and (pos_idx == target_position):
            # This is the target position → now draw the T 
            T_image.pos = coordinates[pos_idx]  # Move the T image to this coordinate (x, y)
            T_image.draw()                      # Queue the T to appear on the next screen flip
        else:
            # All other positions get Ls (the distractor letters)
            L_image.pos = coordinates[pos_idx]   # Move the L image to the current coordinate
            L_image.draw()                       # Queue the L to appear on the next screen flip

    # STEP 5: Now I need to show everything on the screen.
         # Nothing appears until I flip the window.
         # The flip command displays all the queued images (T and Ls) together in one single frame.
    win.flip()

    # STEP 5: Next I need to wait for a key press (1 = present, 0 = absent, ESC = quit the program)
        # event.waitKeys() pauses the experiment until one of these keys is pressed
        # This will return the key the subject pressed 
    response = event.waitKeys(keyList=[Key_Present, Key_Absent, "escape"])  

    # Similar to after the instructions above, if the participant presses ESC, quit the experiment immediately
    if "escape" in response:
        win.close()
        core.quit()

# END OF EXPERIMENT
# Once all trials have finished running, I should likely show some sort of a thank-you message.

ending_text = visual.TextStim(
    win,
    text="Great work! You are all done the experiment.\n\nThank you for participating!\n\nPress ESC to exit.",  
    color="black",
    height=25
)
ending_text.draw()                      # Prepare the text to be displayed on the window
win.flip()                              # Show the thank-you message on the window
event.waitKeys(keyList=["escape"])      # Wait for the subject to press ESC to quit/finish the experiment

win.close()     # Finally, I need to close the window and exit the experiment completely.
core.quit()