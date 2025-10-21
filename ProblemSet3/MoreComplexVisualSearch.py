# Now I will take what I have done previously and start making it a bit more complex
# The only thing I could not figure out was the "take as input the number of trials per condition and participant number"
  # I wasn’t sure how to use PsychoPy’s GUI dialog (gui.DlgFromDict) to collect user input and then integrate those values into the trial generation code.
  # I tried but was unsuccessful and removed what I had done

from psychopy import visual, event, core   # Importing the necessary libraries 
                                           # visual = drawing windows and stimuli (https://www.psychopy.org/api/visual/index.html)
                                           # core = timing/quit (https://www.psychopy.org/api/core.html)
                                           # event = keyboard presses (https://www.psychopy.org/api/event.html)

import csv      # I imported csv here because I want to write to a csv file at the very end 
                # This was not added here originally, so when I went to save it was not working.
                # Here is a site I used when I did save it to a csv file (https://docs.python.org/3/library/csv.html)
                
import random   # Again, importing random becaise I will want to randomize different things at different points

win = visual.Window(fullscr=True, color="white", units="pix") # Creating a window and adding the specifications
                                                              # https://www.psychopy.org/api/visual/window.html 

T_image = visual.ImageStim(win, image="T.png", size=(50, 50))  # This line defines the T stimulus (i.e., the target image).
                                                               # https://www.psychopy.org/api/visual/imagestim.html (used the same for the next visual stim)

L_image = visual.ImageStim(win, image="L.png", size=(50, 50))  # This line defines the L stimulus (i.e., the distractor image).

fixation = visual.TextStim(win, text="+", color="black", height=50, pos=(0, 0)) # This line creates a fixation cross 
                                                                                # https://www.psychopy.org/api/visual/textstim.html

instructions_text = (
    "Welcome to the visual search experiment!\n\n\n"
    "There will be 10 trials for you to complete.\n\n"
    "On each trial, you will see 3, 6 or 9 letters on the screen.\n\n"   # I changed this part to update for mutliple set sizes 
    "Your task is to decide whether there is a letter 'T' amongst the 'L's.\n\n"
    "Press 1 if the 'T' is PRESENT.\n\n"
    "Press 0 if the 'T' is ABSENT.\n\n"
    "Press SPACE to start the experiment.\n\n"
    "Or ESC to leave the experiment."
)
instructions = visual.TextStim(win, text=instructions_text, color="black", height=25, wrapWidth=900, pos=(0, 0))  

instructions.draw()  # Draws the instructions created above (queues it to be flipped later on)
win.flip()           # Flips the instructions onto the screen

keys = event.waitKeys(keyList=["space", "escape"])  # Wait for a subject response 
                                                    # https://www.psychopy.org/api/event.html#psychopy.event.waitKeys

if "escape" in keys:   # If escape is pressed, close and quit experiment
    win.close()
    core.quit()

Num_Trials = 10         # Number of experimental trials
Set_Sizes = [3, 6, 9]   # These are the three possible set sizes (I just added 3 and 6).
Key_Present = '1'       # "1" is the key if a target is present from the search
Key_Absent  = '0'       # "0" is the key if a target is absent from the search

Coordinates = {     # I changed the coordinates this way for each set size and I know this is likely more work than I needed to do
                    # It just made the most sense to me at this moment in time 
                    # I just did not know how to incorporate it into a loop of sorts
                    # It took me a while to figure out how to make them completely centered on the screen each time (for smaller set sizes)
                    
    3: [(-150, 0), (0, 0), (150, 0)],   # 1×3 centered row
    
    6: [(-150, 100), (0, 100), (150, 100),
        (-150, -100), (0, -100), (150, -100)],  # 2×3 centered grid
        
    9: [(-300, 200), (0, 200), (300, 200),
        (-300, 0),   (0, 0),   (300, 0),
        (-300, -200), (0, -200), (300, -200)]   # 3×3 centered grid (this is the same as before- simple experiment)
}

trial_types = [1]*5 + [0]*5    # This creates a list that defines whether each of the 10 trials will have a target (T) or not.
                                   # The [1]*5 part means “make five 1’s” → [1, 1, 1, 1, 1]
                                   # The [0]*5 part means “make five 0’s” → [0, 0, 0, 0, 0]
                                   
random.shuffle(trial_types)    # This randomly shuffles the trial types I defined above (e.g., 1, 0, 0, 1, 1, 0, 1, 0, 1, 0)
                               # https://docs.python.org/3/library/random.html

Distractor_orients = [0, 90, 180, 270]  # Here I added the four different distractor orientations specified in the instructions

Num_practice = 5    # I want at least 5 practice trials so subjects can get the hang of the task

print("Starting the practice trials...")  # I wanted to print to the console that the practice trials are now starting (this is for me)

practice_text =(      # Added a block of instructions for the 5 practice trials
    f"You will first start by completing {Num_practice} practice trials.\n\n"
    "Remember to press '1' if a T is PRESENT, or '0' if the T is ABSENT.\n\n"
    "These practice trials will not be timed.\n\n"
    "But still try to be as fast and accurate as possible.\n\n"
    "Press SPACE to begin.\n\n"
)
practice = visual.TextStim(win, text=practice_text, color="black", height=25, wrapWidth=900, pos=(0, 0)) # These are the practice text speicifcations

practice.draw()   # Again, this draws the practice text (queues it) 
win.flip()        # This flips the text onto the screen

keys = event.waitKeys(keyList=["space", "escape"]) # Wait for a subject response 

if "escape" in keys:    # If escape is pressed, close and quit the experiment
    win.close()
    core.quit()

# This starts the practice trial loop.
for prac_idx in range(Num_practice):   # 'prac_idx' is just a counter (like 0, 1, 2, …) that keeps track of which practice trial we’re on.

    fixation.draw()    # Draw the fixation at the beginning of each trial
    win.flip()         # Flip the fixtaion onto the screen for the subject to see 
    core.wait(0.5)       # Leave it on the screen for 500 ms (half a second).

    present = random.choice([0, 1])          # This randomly makes it target-present or absent trial (https://docs.python.org/3/library/random.html)
    Set_Size = random.choice(Set_Sizes)      # This randomly chooses 3, 6, or 9 for the set size of each trial
    Coordinates_used = Coordinates[Set_Size] # This pulls the correct list of (x, y) coordinates based on the set size chosen above.
    target_position = random.randrange(Set_Size) if present else None # This decides where to place the T (target) IF it’s a target-present trial.

    for pos_idx in range(Set_Size):  # This loop goes through every position (slot) in the current display.
                                     # range(Set_Size) creates a list of numbers (e.g., if Set_Size = 6 → [0,1,2,3,4,5]).
                                     # Each number (pos_idx) corresponds to one position from the Coordinates_used list.
                                     
        if present and (pos_idx == target_position): # This line checks two things:
                                                         #(1) Is the target supposed to be present this trial? (present == 1)
                                                         # (2) Is this specific position the one randomly chosen for the T?
                                                         
            T_image.ori = 0                              # This shows that the target will always be upright (set at 0)
            T_image.pos = Coordinates_used[pos_idx]      # Move the T to this position on screen (based on its (x, y) coordinates).
            T_image.draw()                               # Draw the T image (queue it to be flipped)
            
        else:     # If the above condition is NOT true, that means either:
                     # It's a target-absent trial (ALL L's), OR
                     # This position is NOT the chosen target slot.
                     # In both cases, this position should show a distractor L instead.
            L_image.ori = random.choice([0, 90, 180, 270])   # This randomly chooses a distractor orientation
            L_image.pos = Coordinates_used[pos_idx]          # Move the L to its assigned screen position. 
            L_image.draw()                                   # Again, draw the L image 

    win.flip()    # Flip all stimuli onto the screen so that subjects can see it 
    
    response = event.waitKeys(keyList=[Key_Present, Key_Absent, "escape"])   # Wait for a response (if escape, close and quit the experiment)
    
    if "escape" in response:   # If escape is pressed, close and quit the experiment
        win.close()
        core.quit()
        
    # Now I need to evaluate if the subjects response was correct or not
    resp_key = response[0]     # This grabs the first key pressed (there is only one key to be pressed when they make a decision of pres or abs)
    
    expected = Key_Present if present else Key_Absent  # This means that if the variable present is True (1), set expected to Key_Present.
                                                       # Otherwise, set expected to Key_Absent. 
    
    is_correct = (resp_key == expected)    # If the key the subject pressed matches the expected key (correct key)
                                           # This returns a boolean value - TRUE or FALSE
                                           # For example, if the trial had expected = '1' and the participant pressed '1'
                                              # is_correct = True

    # Now I am building feedback text 
    if is_correct:     # This checks whether the subjects response was correct.
                       # is_correct is either True or False, based on whether their response matched the correct answer.
                       # If it’s True, the code inside this “if” block runs; if it’s False, the else part runs.
        fb_msg = "Correct!"  # Means their response was correct 
    else:
        fb_msg = f"Incorrect. Correct answer: {'1 (T PRESENT)' if present else '0 (T ABSENT)'}"  # This means their response was incorrect
                                                                                                 # Gives them the instructions/task again

    # Next I want to show feedback to participants briefly before the next practice trial begins
    feedback = visual.TextStim(
        win,
        text=fb_msg,
        color="black",
        height=32,
        wrapWidth=900,
        pos=(0, 0)
    )
    feedback.draw()
    win.flip()
    core.wait(1.5)  # This is the feedback duration (I played with a few numbers here but this felt right)

start_maintask = visual.TextStim(    # I added a small message before main trials begin (this also gives the subjects a brief break)
    win,
    text="Practice trials complete!\n\nYou will now be starting the 10 experimental trials.\n\n These trials will be timed.\n\n So try to respond as quickly and accurately as you can.\n\n Press SPACE to begin.",
    color="black",
    height=25
)

start_maintask.draw()   # Draw these instructions (queue it to be flipped)
win.flip()              # Flip them onto the screen

keys = event.waitKeys(keyList=["space", "escape"])  # Again wait for a response from the subject 
if "escape" in keys:     # If escape is pressed, close and quit the experiment
        win.close()
        core.quit()
        
print("Starting experimental trials...")   # I wanted to print to the console that the experimental trials are now starting

rt_clock = core.Clock()        # I am adding simple stopwatch to track RT's per trial
                                    # https://www.psychopy.org/api/clock.html
                                    # I only want to do this for the experimental trials (i.e., the practice trials are NOT timed)
                                    
results = []                   # This empty list will collect a dictionary of data for each of the 10 experimental trials
                                    # Each dictionary = one row of data with labels (e.g., trial, RT, accuracy)
                                    # https://docs.python.org/3/tutorial/datastructures.html#dictionaries

# This is the start of the main experimental loop
for trial_idx in range(Num_Trials):   # The variable 'trial_idx' acts like a counter that keeps track of which trial number we’re on (0, 1, 2, …, 9).
                                      # This loop repeats everything below 10 times total (because Num_Trials = 10 above).
    
    fixation.draw()   # This draws the fixation cross (queues it to be flipped)
    win.flip()        # This flips the fixation onto the window so the subject sees it on the screen
    core.wait(0.5)      # Only appears for 500ms (or half a second)
                      # This will happen at the beginning of every trial

    present = trial_types[trial_idx]   # This line looks up whether the *current trial* should have a target (T) or not.
                                           # 'trial_types' is the list I made earlier with five 1’s (target-present) and five 0’s (target-absent),
                                           # I shuffled it so the order is random each time the experiment runs
    
    Set_Size = random.choice(Set_Sizes)  # I added this line to randomly pick one of the three set sizes
                                         # Does this on a trial by trial basis
                                         
    Coordinates_used = Coordinates[Set_Size]  # This means to get me the list of coordinates that matches the current set size
                                              # i.e., this picks the coordinate layout (3, 6, or 9 positions) for this trial

    target_position = random.randrange(Set_Size) if present else None # This decides *where* the target (T) will appear — only if it’s a target-present trial.

    # This loop goes through every position (coordinate) for this trial’s display.
    for pos_idx in range(Set_Size):    
                # “pos_idx” is just a counter (0, 1, 2, …) that tells me which spot we’re currently filling on the screen.
                # “range(Set_Size)” means the loop will run once for every letter that needs to appear.
                    #e.g., if the Set_Size is 6 → it will run 6 times (once for each letter location).
                # On each loop, this decides whether to draw the target (T) or a distractor (L)
                
        if present and (pos_idx == target_position):   # This checks two things:
                                                            #   1. “present” → is this a target-present trial?
                                                            #   2. “pos_idx == target_position” → are we currently at the coordinate where the T should go?
                                                        # If BOTH are true, it means this is the one spot that should display the T.
                                                        
            T_image.ori = 0    # This makes sure the target image is ALWAYS upright
            T_image.pos = Coordinates_used[pos_idx]   # Move the T to one of those positions within the chosen coordinates 
            T_image.draw()    # Draw the image (queue it to be flipped)
            
        else:   # If we’re NOT at the target position (or it’s a target-absent trial), this draws an L instead — the distractor letter.
            L_image.ori = random.choice(Distractor_orients)   # This randomly chooses the distractor orientations
            L_image.pos = Coordinates_used[pos_idx]   # If else, move the L to one of those positions within the chosen coordinates
            L_image.draw()

    win.flip()   # Flip the stimuli for this trial onto the screen for the subject to see 
    
    rt_clock.reset()    # I first need to reset the RT clock so it starts counting from 0 again for this trial
                           # Each trial will get its own RT starting point
                           # (https://www.psychopy.org/api/core.html#psychopy.core.Clock.reset)
                           # This is where RT's get measured (i.e., starting now when the array appears)
                           # Next I need to wait for the subject to respond.
    
    # I added a simple time-out for responses in experimental trials only (I did not include this in the practice trials)
    response = event.waitKeys(keyList=[Key_Present, Key_Absent, "escape"],
                              timeStamped=rt_clock,
                              maxWait=1.5) # If no key is pressed within 2.0 seconds, this returns None (i.e., timed out)
                                           # I can change 1.5 to any time limit I want (in seconds)
                                           # For me this visual search is a bit hard because the stim are so similar, so I kept it at 1.5

    # But now I want to unpack that tuple so it’s easier to read.
        # If the trial timed out, response will be None — so I need to handle that first
    if response is None:
        resp_key = None      # No key was pressed before the time limit
        rt = None            # No RT recorded 
        # Below, the accuracy line compares None to the expected key and will mark it as incorrect (0).
    else:
        resp_key, rt = response[0]   # "response[0]" grabs the first tuple (e.g., ('1', 0.82))
                                     # "resp_key" = '1' (e.g., the key pressed)
                                     # "rt" = 0.82 (e.g., the time in seconds)
        
        # I also need to include the “escape” option so the subject can stop the experiment at any point 
        if resp_key == "escape":    # So, if ESC is pressed → close the window and quit experiment 
            win.close()
            core.quit()
        
    # Now I need to calculate accuracy for the trial
    expected = Key_Present if present else Key_Absent   # I know whether this trial was target-present or absent (from “present” variable above).
                                                            # If it was present, the correct key should be “1”.
                                                            # But, if it was absent, the correct key should be “0”.
    
    # Next I need to compare what the subject actually pressed to what was the correct press
    correct = int(resp_key == expected)   # If they match, “correct” becomes 1; otherwise it becomes 0.
                                          # (int() just converts True/False into 1/0 for easier saving)
                                          
    # Finally, I need to store the trial data in a list of dictionaries (called “results”).
    #     Each dictionary will hold all the info for one trial — like a row in Excel.
    results.append({
        "trial": trial_idx + 1,             # trial number (1 through however many)
        "set_size": Set_Size,               # how many letters appeared this trial
        "present": present,                 # whether a T was present (1) or absent (0)
        "target_position": target_position, # where the T was shown (None if absent)
        "response": resp_key,               # what key was pressed ('1' or '0') — may be None if it timed out
        "rt": rt,                           # reaction time in seconds — may be None if it timed out
        "correct": correct                  # 1 = correct, 0 = incorrect (timeouts become 0 automatically)
    }) 
    
# I now need to save trial data to a csv file (only the experimental trials) 
with open('visual_search_data.csv', 'w', newline='') as csvfile:  # "open(..., 'w')" = open a new file for writing 
                                                                  # 'newline='' is recommended on Windows so Python doesn't insert extra blank lines in the CSV
                                                                  # Here is a site I used (https://docs.python.org/3/library/csv.html#csv.DictWriter)
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["trial", "set_size", "present", "target_position", "response", "rt", "correct"]
)
            # csv.DictWriter lets me write rows using Python dictionaries (key=value pairs).
            # "fieldnames" defines the column order in the CSV. 
            # The keys in my dictionaries must match these names
            
    writer.writeheader()       # This writes the header row at the top of the CSV: trial,set_size,present,target_position,response,rt,correct
    
    writer.writerows(results)  # This writes each trial's dictionary as one row in the file.
                                    # "results" is my list of dictionaires that I appended to during the experiment
                                    # Example row:{"trial": 1, "set_size": 6, "present": 1, "target_position": 4, "response": "1", "rt": 0.742, "correct": 1}

print("Data saved to visual_search_data.csv")  # This prints a confirmation message to the console so I know the file was successfully written to a csv file

# Now I want to calculate and display the subjects performance on the screen
   # In other words, this section summarizes how well the subject performed overall

#  First I need to create simple counters to track the subjects performance
num_trials = len(results)     # The total number of experimental trials completed
num_correct = 0               # This will count how many trials were correct
total_rt = 0                  # This will add up all RTs from correct trials only
num_rt = 0                    # This will count how many correct RTs were included

# Now I need to loop through every trial in the 'results' list
for trial in results:                        # This goes through each item inside the list called 'results'.
    if trial["correct"] == 1:                # If the trial was correct (1 = correct, 0 = incorrect)
        num_correct = num_correct + 1        # Add 1 to the total number of correct trials (i.e., if correct, add one more to the total)
        total_rt = total_rt + trial["rt"]    # Add that trial's RT to the total RT
        num_rt = num_rt + 1                  # Count that this RT was included

# I next need to compute the subjects accuracy and the mean RT across the 10 trials
accuracy = (num_correct / num_trials) * 100    # Turn accuracy into a percentage (e.g., 80.00%)

if num_rt > 0:                                 # If there were any correct trials
    mean_rt = total_rt / num_rt                # Compute the average RT for only those correct trials
else:
    mean_rt = 0                                # Just in case all responses were wrong (avoids a crash)(learned the hard way)

# Now I want to show a summary screen to the subject with their accuracy and average RT 
summary_text = visual.TextStim(       # I need some help here 
                                      # Everytime I did not include the f's, the output (when flipped onto the screen) would not look right
                                      # Here I asked Chat gpt to debug this for me, and it explained that:
                                         # Without the f-string(f), Python will not insert the variable values — it’ll just show the words literally
                                         # The f before the quotes replaces {accuracy} and {mean_rt} with real numbers.
                                         # With it removed, PsychoPy just prints the curly brackets and variable names literally.
                                         # Here is a site for this as well (https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
    win,
    text=f"Great work! The experiment is now complete!\n\n"  # It also explained that including the f-string (f) within the brackets with a number, will tell it how many decimals to include.
         f"Accuracy: {accuracy:.2f}%\n\n"                    # Included two decimals for readability (“floating-point number" (f) with 2 decimal places) 
                                                                # Here is a site for this as well (https://docs.python.org/3/library/string.html#formatspec_)
         f"Average RT: {mean_rt:.2f} seconds\n\n"            # Also, included two decimals for RTs 
         f"Press ESCAPE to exit.",
    color="black",
    height=25
)

summary_text.draw()    # Draw summary text with the subjects accuracy and average RT included 
win.flip()             # Flip this onto the screen so the subject can see how they performed and also know the experiment is complete

event.waitKeys(keyList=["escape"])   # Waits for escape to be pressed to finish the experimemt

win.close()  # Close and then quit the experiment (we are done)
core.quit()