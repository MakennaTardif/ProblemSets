#-----------------------------------
# 1) IMPORTING NECESSARY LIBRARIES
#-----------------------------------

import os    # https://docs.python.org/3/library/os.html (i.e., tools for listing files, creating directories, and building file paths)
import re    # https://docs.python.org/3/library/re.html (i.e., pattern matching to extract emotion, gender, and ID from filenames)
from psychopy import visual, core, event  # Provides stimulus display (visual), precise timing (core), and input handling (event) for running the experiment
import random  # Used to randomize trial order, face selection, and foil sampling to prevent order effects
import numpy as np # Used to compute evenly spaced circular positions so all faces are equidistant from fixation
from psychopy.visual import Slider # https://www.psychopy.org/api/visual/slider.html (i.e., used to collect continuous percentage estimates)
import csv  # Used to save trial-by-trial data in a clean, analysis-ready CSV format
from datetime import datetime # https://www.geeksforgeeks.org/python/python-datetime-module/ (i.e., used to timestamp participant files & trial entries for data management/traceability)

# I import csv + datetime here so BOTH the grid task and the memory task can write to the SAME file with timestamps.
# Keeping one CSV per participant makes it way easier to match estimates + memory performance later.

# --------------------------------------------
# 2) PRELOADING ALL (NOW SMALLER) STIM IMAGES
#---------------------------------------------

# After resizing the images, I can now load the images into PsychoPy.
# Preloading ensures that each ImageStim is ready when needed, which reduces delays during the trial sequence.

# First, I need to create a setup window
win = visual.Window(fullscr=True, color="white", units="pix") 
    # fullscr=True is important because positions/sizing are consistent across participants (less messing around with window size differences).

# Now I can preload stim images
stim_folder = "stimuli_small"   # Using the resized images (without the "_small" it would use the original large images
                                # This folder should contain BOTH the normal identity images AND the foil images (foils have "Foil" in the name).

# Pattern for filenames like: AngryFemale1, HappyMale2, NeutralFemale12, etc.
pattern = re.compile(r"(Angry|Happy|Neutral)(Female|Male)(\d+)", re.IGNORECASE)  # Extract the emotion, gender, and ID number from each filename
                                                                                 # re.IGNORECASE allows filenames with any capitalization
                                                                                 # This regex pattern is ONLY for the "real" identity faces (it intentionally does NOT match Foil files).
                                                                                 # That’s why foils have to be loaded separately later in the memory section.
                                                                                 # https://www.geeksforgeeks.org/python/python-re-compile/

image_cache = {}      # Dictionary that stores each stimulus and its info, indexed by (identity, emotion)
identities_info = []  # List storing identity + gender pairs

# Loop through every file in the stimuli folder
for fname in os.listdir(stim_folder):    # os.listdir() in Python is a built-in function from the os module that returns a list of all files and directories in a given path.
                                         # https://www.w3schools.com/python/ref_os_listdir.asp
                                         # https://docs.python.org/3/library/os.path.html

    # Only use jpg files
    if not fname.lower().endswith(".jpg"): # This prevents non-image junk files (like .DS_Store) from crashing the preload loop.
        continue

    # Remove the .jpg extension
    stem = os.path.splitext(fname)[0]  # https://docs.python.org/3/library/os.path.html

    # Try to match the naming pattern
    m = pattern.fullmatch(stem)    # If the filename matches the pattern → m becomes a match object containing the extracted groups (emotion, gender, number).
                                   # https://www.pythontutorial.net/python-regex/python-regex-fullmatch/

    if not m:  # Skip files that don’t follow the emotion–gender–number naming pattern
        print("Skipping (name doesn’t match pattern):", fname) # This will skip ALL foil files, because they have "Foil" in the name and don’t match this pattern.
        continue

    # Extracting the emotion, gender, number
    emo, sex_raw, num = m.groups()  # Extract emotion, gender text, and number from the filename match
                                    # https://stackoverflow.com/questions/20202365/the-groups-method-in-regular-expressions-in-python

    emotion = emo.lower()     # Convert emotion string to lowercase for consistency
                              # https://www.w3schools.com/python/ref_string_lower.asp
                              
    gender  = "female" if sex_raw.lower() == "female" else "male"  # Mapping gender text to a standard label
    
    identity = f"{gender[0].upper()}{num}"  # Create compact ID like "F1" or "M12"
                                            # I turn identity into "F1/M1" style codes because they are short and easy to store in CSVs and analyze later.

    # Full path to the file
    path = os.path.join(stim_folder, fname) # https://www.geeksforgeeks.org/python/python-os-path-join-method/

    # Preload the image into PsychoPy (the display size can stay 240×180 to match the resized files)
    stim = visual.ImageStim(win, image=path, size=(240, 180), autoLog=False) # Preloading ImageStim objects is important so the grid shows smoothly (less lag between faces).


    # Store everything in the cache so I can retrieve it later during the experiment
    image_cache[(identity, emotion)] = {
        "stim": stim,       # The actual PsychoPy ImageStim object for this face
        "gender": gender,   # The gender label extracted from the filename ("female" or "male")
        "emotion": emotion, # The emotion label extracted from the filename ("angry", "happy", "neutral")
        "id": identity,     # The compact identity code I created (e.g., "F1", "M12")
        "path": path,}      # The full file path to this resized stimulus image

    # Store identity–gender pair 
    identities_info.append((identity, gender))  # Stores simple (identity, gender) pairs, which may be used later for counterbalancing, stimulus selection, or debugging.
                                                # https://www.w3schools.com/python/ref_list_append.asp

# Summary printout
print(f"Preloaded {len(image_cache)} identity×emotion images.")  # Confirm in the console that images have been preloaded
                                                                 # This number should be 108 if you have 36 identities per gender × 3 emotions.
                                                                 # If it’s lower, it means your folder naming pattern or missing files need fixing.
# -------------------------------------------------
# 3) GRID TASK + 3 SLIDERS (that must sum to 100%)
# -------------------------------------------------

# BALANCED SUBJECT GROUP ASSIGNMENT (1→2→3→1→2→3…)

GROUP_COUNTER_FILE = "group_counter.txt"
# Name of a small text file used to keep track of how many participants have already been run, so subject groups can be assigned evenly.
    # This is really ONLY needed if I was running people one-by-one locally (which I may do at some point) and want automatic balancing.
    # But if I do run online (or my CSV already stores group), I can assign group another way and skip this file.

def get_balanced_subject_group(counter_file=GROUP_COUNTER_FILE):
    # The function that assigns participants to subject groups (1, 2, or 3) in a rotating order to keep group sizes approximately equal.

    if not os.path.exists(counter_file):  # https://docs.python.org/3/library/os.path.html
        # If the counter file does not yet exist (e.g., first participant), create it so we have something to read from.
        with open(counter_file, "w") as f:
            f.write("0")
            # Initialize the counter at 0 (i.e., no participants yet).

    with open(counter_file, "r") as f:
        # Open the counter file to read how many participants have already run.
        txt = f.read().strip()
        # Read the contents and remove any extra whitespace.
        count = int(txt) if txt != "" else 0
        # Convert the stored value to an integer.
            # If the file is empty for some reason, default to 0.

    subject_group = (count % 3) + 1
    # Assign subject group using modulo arithmetic:
        # count % 3 cycles through 0, 1, 2 + 1 converts this to group numbers 1, 2, 3
            # This produces the pattern: 1, 2, 3, 1, 2, 3, ...
                # This is the cleanest way to rotate people through 3 groups without manually tracking it.

    with open(counter_file, "w") as f:
        # Reopen the counter file in write mode to update the participant count.
        f.write(str(count + 1))
        # Increment the counter so the next participant is assigned to the next subject group.

    participant_index = count + 1
    # Assign a participant index based on run order.
        # This provides a simple unique identifier for each participant.

    return subject_group, participant_index
    # Return both the assigned subject group and participant index so they can be logged in the data file.

subject_group, participant_index = get_balanced_subject_group()
# Call the function to assign the current participant to a subject group and obtain their participant index.

print(f"Participant index {participant_index} assigned to Subject Group {subject_group}")
# Print confirmation to the console so the experimenter can verify that the participant was assigned correctly.
    # I print this so I can confirm the script is rotating properly while I’m testing.

# SUBJECT GROUP EMOTION ROTATION
    # base 0/1/2 map differently by group
        # Group 1: base0->angry,  base1->happy,  base2->neutral
        # Group 2: base0->happy,  base1->neutral,base2->angry
        # Group 3: base0->neutral,base1->angry,  base2->happy
    # This counterbalancing ensures that identities are not consistently paired with the same emotion across participants.
        # This is important because it prevents one specific identity set from always being "angry" for everyone.
            # So any bias we may see is less likely to be driven by a weird identity subset.

emotions_cycle = ["angry", "happy", "neutral"]
# Defines a fixed ordering of emotion labels that will be rotated depending on the participant’s subject group.

offset = subject_group - 1
# Converts subject group (1, 2, or 3) into a zero-based offset (0, 1, or 2) so it can be used in modular arithmetic.

def base_to_emotion(base_index):
    # Function that converts a base set index (0, 1, or 2) into the actual emotion shown on that trial for this participant.
    return emotions_cycle[(base_index + offset) % 3]
        # Adds the subject-group offset and wraps around using modulo 3, producing the correct emotion mapping for the current group.
        # Using modulo here is how I "rotate" the mapping without writing 3 separate if-statements.

# GETTING AVAILABLE IDENTITIES BY GENDER (from image_cache)
    # This section organizes identities so trials can be built separately for male and female faces.

ids_by_gender = {"female": set(), "male": set()}
# Initialize a dictionary where each gender maps to a set of identities.
    # Sets are used to avoid duplicate identity entries.

for (identity, emotion), info in image_cache.items():
    # Loop through each (key, value) pair in the dictionary (i.e., the image cache).
        # The key is a tuple (identity, emotion), which Python automatically unpacks.
    ids_by_gender[info["gender"]].add(identity)
    # Add the identity to the appropriate gender set.
        # Using a set ensures each identity only appears once per gender.
        # I do this because I want “female-only grids” and “male-only grids” as separate trial types.

# Convert to sorted lists (this is nice for debugging)
ids_by_gender = {g: sorted(list(s)) for g, s in ids_by_gender.items()} # Sorting makes the contents predictable and easier to inspect or debug.
                                                                       # https://docs.python.org/3/library/functions.html#sorted

# Confirm each identity has all 3 emotions in cache
    # This is a safety check to ensure the stimulus set is complete.
for g in ["female", "male"]:
    # Loop over both genders separately.
    for ident in ids_by_gender[g]:
        # Loop over every identity belonging to the current gender.
        for emo in ["angry", "happy", "neutral"]:
            # Check that all three emotion versions exist for this identity
            if (ident, emo) not in image_cache:
                # If any emotion version is missing, stop the experiment and raise a clear error explaining what is wrong.
                raise ValueError(f"Missing stimulus for identity {ident} emotion {emo} (gender {g}).")
                    # This prevents silent bugs where one emotion version is missing and PsychoPy would crash mid-experiment.

# BUILDING 3 TRIALS PER GENDER USING THE BASE SETS (0/1/2)
    # Each trial uses 2 ids from each base set => 6 faces per trial.
    # Because base-> emotion is just a permutation per group, each grid will ALWAYS contain 2 angry, 2 happy, 2 neutral.

def make_gender_trials(gender, rng):
    # Function that creates all grid trials for a single gender (male or female).
        # Each gender contributes 3 trials, with 6 faces per trial.
    available_ids = ids_by_gender[gender]
    # Retrieve the list of available identities for the specified gender.

    # Need 18 unique identities per gender (3 trials × 6 faces)
    if len(available_ids) < 18:
        # Safety check: To ensure there are enough identities to build all trials.
        raise ValueError(f"Need at least 18 identities for gender {gender}, but found {len(available_ids)}.")

    chosen = rng.sample(available_ids, 18) # https://numpy.org/doc/stable/reference/random/generator.html
    # Randomly select 18 unique identities for this gender.
        # These identities will be distributed across the 3 grid trials.
            # This means each identity is seen only ONCE in the whole grid task (prevents repetition effects).

    base0 = chosen[0:6]
    base1 = chosen[6:12]
    base2 = chosen[12:18]
    # Split the 18 identities into three base sets of 6 identities each.
        # These base sets correspond to base indices 0, 1, and 2.
        # Emotion assignment will be determined later using subject-group rotation.

    trials = []
     # Initialize an empty list to store the three trials for this gender.
     
    for t in range(3):
        # Loop over the three trials to be created.
        trial = []
        # Start with an empty trial list.
        trial += [(0, gender, ident) for ident in base0[2*t:2*(t+1)]]
        # Add two identities from base set 0 to this trial.
            # These identities are tagged with base index 0.
        trial += [(1, gender, ident) for ident in base1[2*t:2*(t+1)]]
        # Add two identities from base set 1 to this trial.
            # These identities are tagged with base index 1.
        trial += [(2, gender, ident) for ident in base2[2*t:2*(t+1)]]
        # Add two identities from base set 2 to this trial.
            # These identities are tagged with base index 2.
        rng.shuffle(trial)
        # Randomize the order of the six faces around the circle so that position is not systematically linked to base set or emotion.
        trials.append(trial)
        # Store the completed trial.
    return trials
    # Return a list containing three trials for the specified gender.

rng = random.Random()  # https://docs.python.org/3/library/random.html#random.Random
# Create a random number generator instance.
    # Using a dedicated RNG allows controlled and reproducible randomization if needed.

female_trials = make_gender_trials("female", rng)
# Generate the three grid trials containing ONLY female faces.

male_trials   = make_gender_trials("male", rng)
# Generate the three grid trials containing ONLY male faces.

all_trials = female_trials + male_trials
# Combine the male and female trials into a single list of six trials total.

rng.shuffle(all_trials)  # https://docs.python.org/3/library/random.html#random.shuffle
# Randomize the order of the six grids so that gender order is not predictable.
    # This makes it so participants don’t always see “female first then male” which could create order effects.

# POSITIONS ON A CIRCLE

n_positions = 6
# Specifies the number of face positions to place around the circle.
    # This matches the number of faces shown on each grid (6 total).
    
radius = 250
# Sets the distance (in pixels) from the central fixation point to each face.
    # Because all faces use the same radius, they are all equally distant from fixation.
    
angles = np.linspace(0, 2*np.pi, n_positions, endpoint=False) + (np.pi/2)
# Creates six evenly spaced angles around a full circle (0 to 2π).
    # Adding π/2 rotates the entire circle so that one face is positioned directly above fixation, which looks more intuitive as a circular layout.
    # https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    # https://numpy.org/doc/stable/reference/constants.html

circle_positions = [(radius*np.cos(a), radius*np.sin(a)) for a in angles]
# Converts each angle into (x, y) screen coordinates using cosine and sine.
    # This produces six positions that are evenly spaced around a circle and all exactly the same distance from the center fixation point.
    # This also guarantees equal distance from fixation (so location is not a confound).
    # https://numpy.org/doc/stable/reference/generated/numpy.sin.html
    # https://numpy.org/doc/stable/reference/generated/numpy.cos.html

# FIXATION CROSS & TASK INSTRUCTIONS 

# Creating a fixation cross (to appear before each grid)
fixation = visual.TextStim(win, text="+", color="black", height=45, font="Arial", bold=True) 

# Creating a set of instructions for the begginning 
start_instructions = visual.TextStim(
    win,
    text=(
        "WELCOME TO THE EXPERIMENT!\n\n\n"

        "In this first section, you will briefly see 6 faces arranged in a circle.\n\n"
        
        "Please look at the entire set of faces while they are on the screen.\n\n"

        "After the faces disappear, you will estimate the percentage of faces that showed each emotion:\n\n"
        
        "  • Angry\n"
        "  • Happy\n"
        "  • Neutral\n\n"
        
        "Use the sliders on the screen to make your estimates. Note, the sliders must add up to 100%.\n\n"
        
        "You will repeat this process for multiple sets of faces.\n\n"

        "Press SPACE to begin."),
    color="black",
    wrapWidth=1000, # Controls how wide the text can be before wrapping to a new line, keeping instructions readable without stretching across the full screen.
    font="Arial",
    height=28,
    bold=False)  # I tried to have this all bolded but I did not like it

start_instructions.draw()  # Draws the instruction text to the back buffer.

win.flip()   # Updates the screen to display everything that has been drawn.
             # This makes the instructions visible to the participant.

event.waitKeys(keyList=["space"])  # Pauses the experiment and waits until the participant presses the SPACE key.

event.clearEvents()  # Clears any remaining keypress events from the buffer.
                     # Prevents the SPACE press used to start the task from being accidentally registered as a response in the next part of the experiment.


# THREE SLIDERS (0–100 by 5) that MUST sum to 100%

# Slider tick values (0–100 in steps of 5 - this is typical of sliders I have used before)
ticks = list(range(0, 101, 5))

# PREDEFINING SLIDER LABELS
    # IMPORTANT: The labels list must match the length of ticks.
    # Only major values are labeled; others are left blank.
slider_labels = [
    "0"   if t == 0   else
    "25"  if t == 25  else
    "50"  if t == 50  else
    "75"  if t == 75  else
    "100" if t == 100 else ""
    for t in ticks]
    # I am doing this because PsychoPy expects a label slot for every tick, even if most ticks are blank.
    # https://docs.python.org/3/reference/expressions.html#conditional-expressions
    # https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions

# COMMON SLIDER SETTINGS
    # Using a shared dictionary keeps the code cleaner and ensures all three sliders are visually identical.
        # Larger size + explicit lineColor makes the slider track visible against a white background.
        
slider_kwargs = dict(   # Creates a dictionary of shared settings for the sliders.
                        # https://docs.python.org/3/tutorial/controlflow.html#keyword-arguments
    win=win,                # Specifies the PsychoPy window in which the slider will be drawn.
    ticks=ticks,            # Defines the numeric scale of the slider (here, 0–100 in 5% steps), which determines the possible response values.
    granularity=5,          # Sliders move in fixed 5% increments
    size=(900, 60),         # Larger size so sliders look like real UI elements
    labels=slider_labels,   # Predefined labels 
    labelHeight=26,         # Larger numbers for readability
    style=("slider"),       # Chose slider because I wanted a slider to appear for this section
    color="black",          # Sets the primary color of the slider elements so they are clearly visible against a white background.
    fillColor="red",        # Sets the color of the filled part (I tried different colors but I liked red)
    markerColor="black",    # Sets the color of the slider’s marker/handle 
    lineColor="black",      # Ensures the slider bar itself is visible
    font="Arial")           # Font type

# CREATING THE THREE EMOTION SLIDERS
    # Positions are vertically spaced but kept fairly tight so the screen does not feel overly sparse.
    
angry_slider   = Slider(pos=(0,  180), **slider_kwargs)
    # Creates the slider used to estimate the percentage of angry faces.
        # The position places it near the top of the slider panel.
happy_slider   = Slider(pos=(0,    0), **slider_kwargs)
    # Creates the slider used to estimate the percentage of happy faces.
        # This slider is centered vertically on the screen.
neutral_slider = Slider(pos=(0, -180), **slider_kwargs)
    # Creates the slider used to estimate the percentage of neutral faces.
        # The position places it near the bottom of the slider panel.

# SLIDER TEXT LABELS (i.e., the emotion names)
    # These are separate TextStim objects so the font size and placement can be controlled independently of the sliders themselves.

label_kwargs = dict(  # Common label settings (this is defined once for efficiency and consistency)
    win=win,
    color="black",
    font="Arial",
    bold=True,
    height=26)

angry_label = visual.TextStim(  # https://www.psychopy.org/api/visual/textstim.html
    text="Angry (%)", pos=(-560,  180),
    **label_kwargs)
    # Creates the text label for the Angry slider.

happy_label = visual.TextStim(
    text="Happy (%)", pos=(-560,    0),
    **label_kwargs)
    # Creates the text label for the Happy slider.

neutral_label = visual.TextStim(
    text="Neutral (%)", pos=(-560, -180),
    **label_kwargs)
    # Creates the text label for the Neutral slider.

# Instruction text shown above the sliders
prompt = visual.TextStim(
    win,
    text="Adjust the sliders. Press SPACE only when the total is equal to 100%.",
    pos=(0, 320),
    color="black",
    font="Arial",
    bold=True,
    height=28)

# Text showing the running total of the three sliders
    # This updates dynamically while the participant adjusts the sliders.
total_text = visual.TextStim( # total_text is the “gatekeeper” so I only let a participant continue when the sum is exactly 100.
    win,
    text="Total: 0",
    pos=(0, -320),
    color="black",
    font="Arial",
    bold=True,
    height=28)

# LOGGING: Exact 36 faces presented and trial estimates

seen_faces = []  # seen_faces is essential because it tells me exactly what the participant saw (needed for the memory task “old” list).
seen_keys  = set()
grid_estimates = []

# -------------------------
# 4) CREATING A .CSV FILE 
# -------------------------

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)
    # This auto-creates a clean “data” folder so participant files aren’t scattered in the main project folder.
    # https://docs.python.org/3/library/os.html#os.makedirs

timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S") 
    # This creates a time stamp string like 20251218_142530 (YYYYMMDD_HHMMSS) based on the current date/time.
        # I use this so every participant file name is unique (so I never overwrite a file by accident).
        # It also helps with traceability later (I can see exactly when that participant ran).
    # https://docs.python.org/3/library/datetime.html#datetime.datetime.now
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

csv_filename = os.path.join(
    data_folder,
    f"gridEstimates_sub{participant_index:03d}_group{subject_group}_{timestamp_str}.csv")
        # This builds the full path + filename for the output CSV inside the "data" folder.
            # os.path.join makes the path work correctly across computers (Windows/Mac).
            # participant_index:03d pads the number to 3 digits (e.g., 1 → 001), which keeps files neatly ordered.
            # I include subject_group and the timestamp in the filename so I can quickly see the condition + run time.

csv_fieldnames = [ # Will indicate which part of the experiment this row belongs to.
    "task",                   # "grid" or "memory" (this is needed because both parts are saved in the same file)
    "participant_index",      # Participant #
    "subject_group",          # Subject group 1, 2, or 3
    "trial_index",            # Trial (1, 2, 3, 4, 5.......)
    "datetime_local",         # Date and time completed

    "trial_gender_code",      # 1 = male, 2 = female (GRID ONLY)
    "trial_gender_label",     # "male" or "female" (GRID ONLY)
    "angry_estimate",         # % angry
    "happy_estimate",         # % happy
    "neutral_estimate",       # % neutral
    "total",                  # Has to be 100%
    "identities_shown",       # Which identities were shown on each trial
    "emotions_shown",         # Which emotions were shown on each trial

    "memory_identity",        # Itentity shown
    "memory_gender",          # Gender shown
    "memory_emotion",         # Emotion shown
    "old",                    # 1 = old (seen), 0 = foil (new) 
    "response",               # 1 = YES, 0 = NO 
    "correct",                # 1 = correct, 0 = incorrect 

    # NEW (EMOTION RATINGS TASK) COLUMNS
    "rating_identity",        # Identity being rated (should be one of the 36 OLD identities, not a foil)
    "rating_gender",          # Gender of the face being rated
    "rating_emotion",         # Emotion version being rated (angry/happy/neutral, based on what they saw in the grid task)
    "negativity_rating"       # 1–9 negativity rating (1=very positive, 5=neutral, 9=very negative)
]

# I keep ALL columns in one file, and for each row I fill only what applies.
    # That’s why grid rows leave memory columns blank, and memory rows leave grid columns blank.

csv_file = open(csv_filename, "w", newline="", encoding="utf-8")
    # This opens the CSV file for writing (one file per participant).
    
csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames)  # https://docs.python.org/3/library/csv.html#csv.DictWriter
    # This sets up a writer that saves each row using the column names defined above.

csv_writer.writeheader()  # https://docs.python.org/3/library/csv.html#csv.DictWriter.writeheader
    # This writes the column headers at the top of the CSV file.

print(f"Saving grid + memory + ratings data to: {csv_filename}")
    # This prints the file path so I can confirm where the data is being saved.

# ---------------------------------------
# 5) RUNNING THE GRID & ESTIMATION LOOP
#---------------------------------------

# Loop through each grid trial, numbering them starting at 1 for clean trial indexing in the data file.
for trial_index, trial in enumerate(all_trials, start=1):  # https://docs.python.org/3/library/functions.html#enumerate
                                                           # https://docs.python.org/3/tutorial/datastructures.html#looping-techniques

    fixation.draw()  # Drawing the fixtaion
    win.flip()       # Flipping the fixation onto the screen before the grid
    core.wait(0.5)   # Stays on the screen for 500 ms

    # Trial entries: (base_index, gender, identity)
    identities_this_trial = []  # This stores the identities of the 6 faces shown on the current grid trial.
    emotions_this_trial   = []  # This stores the emotions shown for each of the 6 faces on the current grid trial (after the subject-group rotation).
    trial_gender_label = None   # This will store whether this grid contained male or female faces (this is set during stimulus drawing).

    for stim_spec, pos in zip(trial, circle_positions): # https://docs.python.org/3/library/functions.html#zip
        # Loops over the 6 faces in the current trial and their corresponding circular positions.
        
        base_index, gender, identity = stim_spec
            # Unpacks the trial specification:
                # base_index = which base set the face came from (0, 1, or 2)
                # gender = whether this face is male or female
                # identity = the unique identity code for the face (e.g., F3, M12)
                
        emotion = base_to_emotion(base_index)  
            # Converts the base index into the actual emotion shown on this trial,
                # This is based on the participant’s subject group (i.e., applies the emotion rotation).

        # This should always be either "male" OR "female" for the entire trial
        trial_gender_label = gender
            # Stores the gender for this grid.
                # Because each grid is single-gender, this value will be the same for all 6 faces
                # This can be safely logged once for the entire trial.

        stim = image_cache[(identity, emotion)]["stim"]
            # Retrieves the correct ImageStim from the cache, using the specific identity and the emotion assigned for THIS participant’s group.
        
        stim.pos = pos
            # Assigns the face to its position on the circle, ensuring all faces are equally spaced around fixation.
        
        stim.draw()
            # Draws the face to the screen buffer.
            # The image will actually appear only after win.flip() is called.
        
        # Keeping track of exactly what 6 faces appeared on THIS trial
        identities_this_trial.append(identity)
            # Adds the identity code (e.g., F3, M12) to a list for this trial.
            # This allows me to later log exactly which faces were shown on each grid.
            
        emotions_this_trial.append(emotion)
            # Adds the emotion actually shown for that identity on this trial.
            # This is important because emotion depends on subject group counterbalancing, not just the base identity.

        # Log each identity once (this will become exactly 36 total)
        if identity not in seen_keys:
            # Checks whether this identity has already been logged.
            # This prevents the same face from being counted multiple times across grids.
            seen_keys.add(identity)
                # Adds the identity to a set so we can quickly check it in the future.
                # Using a set makes this fast and guarantees uniqueness.
            seen_faces.append({
                # Stores the full information for this identity the first time it appears.
                # By the end of the grid task, this list will contain exactly 36 unique faces, which are later used to build the memory task (OLD items).
                "participant_index": participant_index,
                "subject_group": subject_group,
                "identity": identity,
                "gender": gender,
                "emotion_shown": emotion})

    win.flip()
        # Updates the screen so the grid of faces actually appears to the participant
    
    core.wait(2.0)
        # Keeps the grid on the screen for 2000 ms before it disappears.
        # This controls exposure time and ensures all participants view the faces for the same duration.

    event.clearEvents()
        # This stops any held-down keys from affecting the slider screen.

    angry_slider.reset()
    happy_slider.reset()
    neutral_slider.reset()

    # reset() is important because we want each grid estimate to start fresh at 0.
        # Helps to not carry over any values from the previous trial.

    while True:
        a = angry_slider.getRating() or 0
        h = happy_slider.getRating() or 0
        n = neutral_slider.getRating() or 0
        total = a + h + n
        # Continuously read the current value of each slider.
            # If a slider has not been moved yet, getRating() returns None,
            # So "or 0" ensures the value defaults to 0 instead of crashing.

        total_text.text = f"Total: {int(total)} (must equal 100)"
            # Update the on-screen total dynamically so participants can see whether their three estimates sum to 100%.

        prompt.draw()
        angry_label.draw(); angry_slider.draw()
        happy_label.draw(); happy_slider.draw()
        neutral_label.draw(); neutral_slider.draw()
        total_text.draw()
            # Redraw all slider elements and text on every frame so the display updates smoothly as the participant adjusts the sliders.
        
        win.flip()
            # Push everything drawn on this frame to the screen.
            # This loop keeps running until the participant presses SPACE with total = 100.

        keys = event.getKeys()   # https://www.psychopy.org/api/event.html#psychopy.event.getKeys
            # Check whether the participant has pressed any keys since the last screen refresh.
            
        if "escape" in keys:
            csv_file.close()
                # Immediately close the CSV file to ensure all data collected so far is safely saved.
            
            core.quit()
                # Exit the experiment cleanly.
                # This provides an emergency quit option for the experimenter or participant.

        if "space" in keys and total == 100:
            # Only allow the participant to continue if:
                # (1) they press SPACE and
                # (2) the three sliders sum exactly to 100%.
           
           # Save estimates for this grid (in a Python list for backup and/or later use)
            grid_estimates.append({
                "participant_index": participant_index, # Identifies which participant provided this estimate.
                                                        # Matches the participant index used in the filename.
                "subject_group": subject_group,  # Records which counterbalancing group (1, 2, or 3) this participant belongs to.
                "trial_index": trial_index,    # Indicates which grid trial this estimate corresponds to (1–6).
                "trial_gender_label": trial_gender_label, # Stores whether this grid contained male or female faces.
                "angry_estimate": int(a),   # Participant’s estimated percentage of angry faces on this grid.
                "happy_estimate": int(h),   # Participant’s estimated percentage of happy faces on this grid.
                "neutral_estimate": int(n), # Participant’s estimated percentage of neutral faces on this grid.
                "total": int(total)})       # Stores the summed total (should always equal 100 at this point).

            trial_gender_code = 1 if trial_gender_label == "male" else 2
                # Convert gender label to code (1 = male, 2 = female)

            # Save estimates for this grid (i.e., into a CSV)
            csv_writer.writerow({                                    # Write one row of grid-task data to the CSV file
                "task": "grid",                                      # Marks this row as belonging to the grid task
                "participant_index": participant_index,              # Identifies which participant produced this row
                "subject_group": subject_group,                      # Records the counterbalancing group (1, 2, or 3)
                "trial_index": trial_index,                          # Indicates which grid trial this is (1–6)
                "datetime_local": datetime.now().isoformat(timespec="seconds"),  # Saves the exact local time the response was recorded
                "trial_gender_code": trial_gender_code,              # Numeric code for gender shown on this grid (1=male, 2=female)
                "trial_gender_label": trial_gender_label,            # Text label for gender shown ("male" or "female")
                "angry_estimate": int(a),                            # Percentage estimate for angry faces on this grid
                "happy_estimate": int(h),                            # Percentage estimate for happy faces on this grid
                "neutral_estimate": int(n),                          # Percentage estimate for neutral faces on this grid
                "total": int(total),                                 # Sum of all three estimates (should always be 100)
                "identities_shown": ";".join(identities_this_trial), # Exact identities shown on this grid (semicolon-separated)
                "emotions_shown": ";".join(emotions_this_trial),     # Actual emotion versions shown for each identity
                
                "memory_identity": "",                               # Blank because this is not a memory trial
                "memory_gender": "",                                 # Blank for grid trials
                "memory_emotion": "",                                # Blank for grid trials
                "old": "",                                           # Blank (only relevant for memory task)
                "response": "",                                      # Blank (only relevant for memory task)
                "correct": "",                                       # Blank (only relevant for memory task)

                "rating_identity": "",                               # Blank (only relevant for ratings task)
                "rating_gender": "",                                 # Blank (only relevant for ratings task)
                "rating_emotion": "",                                # Blank (only relevant for ratings task)
                "negativity_rating": ""})                            # Blank (only relevant for ratings task)

            csv_file.flush()
                # Make sure it writes immediately (so I do not lose any data if it crashes later)

            break
                # Exits the slider loop and moves on to the next grid trial

#-----------------
# 4) MEMORY TASK
# ----------------

# The memory task MUST come AFTER the grid loop finishes
    # This is because we need the full list of 36 faces the participant actually saw (seen_faces).
    # This ordering matters because the memory task depends on the “seen_faces” list being complete.

# MEMORY TASK INSTRUCTIONS

memory_instructions = visual.TextStim( # Creating a new set of instructions to appear after the grid/estimation phase 
    win,
    text=(
        "In this next portion of the study, you will view faces one at a time.\n\n"
        
        "This time you will be asked whether you remember seeing the exact picture of each face.\n\n"
        
        "Some pictures are from the previous section of the experiment and some are new.\n\n"
        
        "Take your time and answer carefully.\n\n"
        
        "Click YES if you saw this picture previously.\n\n"
        
        "However, click NO if you did not see this picture previously.\n\n"
        
        "Press SPACE to begin."
    ),
    color="black",
    wrapWidth=1000,
    font="Arial",
    height=28,
    bold=False)
    
    # I keep the memory instructions separate so it feels like a new “phase” of the experiment for participants.

memory_instructions.draw()             # Draws the memory task instructions to the screen buffer
win.flip()                             # Displays the instructions on the screen
event.waitKeys(keyList=["space"])      # Pauses the experiment until the participant presses SPACE
event.clearEvents()                    # Clears the key buffer so the SPACE press does not carry over to the next task

# BUILDING THE MEMORY TRIAL LIST (OLD + FOILS)

old_trials = []
    # Store the 36 faces the participant actually saw (OLD items)
    # I built a clean list of dicts that includes a PsychoPy ImageStim for each trial.

for f in seen_faces:                  # Loop over every face the participant actually saw during the grid task
    old_trials.append({               # Add this face as an OLD item in the memory task list
        "identity": f["identity"],    # Store the identity code for this face (e.g., F3, M12)
        "gender": f["gender"],        # Store the gender of the face for later analysis
        "emotion": f["emotion_shown"],   # Store the emotion that was shown during encoding
        "old": 1,                        # Mark this item as OLD (previously seen)
        "stim": image_cache[(f["identity"], f["emotion_shown"])]["stim"]}) # Retrieve the exact ImageStim used during the grid task
        
    # Each old trial stores the EXACT emotion version they saw (important, because identities have 3 emotion versions).


# FOIL LOADING (IMPORTANT)
    # Foils were NOT loaded into image_cache because the preload regex skips filenames containing "Foil".
    # So I need to scan the folder and manually load foils here.

foil_trials = []
    # Initialize an empty list that will store all FOIL (new/unseen) faces for the memory task

foil_pattern = re.compile(r"(Angry|Happy|Neutral)(Female|Male)Foil(\d+)", re.IGNORECASE)  # https://docs.python.org/3/library/re.html#re.compile
                                                                                          # https://docs.python.org/3/library/re.html#re.IGNORECASE
    # Regex pattern that matches foil filenames and extracts emotion, gender, and foil number regardless of capitalization
    # Pattern for foil filenames like: AngryFemaleFoil1.jpg, HappyMaleFoil9.jpg, etc.

for fname in os.listdir(stim_folder):
    # Loop through every file in the stimulus folder so we can locate and load foil images
    
    if not fname.lower().endswith(".jpg"):  # Only use jpg files
        continue
        
    if "foil" not in fname.lower():  # Only keep foil files
        continue

    stem = os.path.splitext(fname)[0] # Remove the .jpg extension

    m = foil_pattern.fullmatch(stem)  # Check whether the filename exactly matches the expected foil naming convention
    if not m:   # If the filename does not match the foil pattern
        print("Skipping foil (name doesn’t match foil pattern):", fname)  # Print a message so mismatched files are visible during debugging
        continue  # Skip this file and move on to the next one

    emo, sex_raw, foil_num = m.groups()  # Extract the emotion label, raw gender string, and foil number from the filename

    foil_emotion = emo.lower()  # Convert the emotion label to lowercase for consistency with the rest of the code

    foil_gender  = "female" if sex_raw.lower() == "female" else "male" # Standardize the gender label to "female" or "male"

    foil_identity = f"{foil_gender[0].upper()}Foil{foil_num}" # Create a unique foil identity code (e.g., "FFoil1" or "MFoil9")

        # I label foil identities differently (Foil) so they can NEVER be confused with real identities in analysis.

    foil_path = os.path.join(stim_folder, fname)
        # Full path to the foil file

    foil_stim = visual.ImageStim(win, image=foil_path, size=(240, 180), autoLog=False)
        # Load foil ImageStim NOW (so I can use it in the memory task)

    foil_trials.append({               # Add this foil face as a single memory trial
        "identity": foil_identity,     # Store the unique foil identity code (e.g., "FFoil1")
        "gender": foil_gender,         # Store the gender of the foil face ("male" or "female")
        "emotion": foil_emotion,       # Store the emotion shown on the foil face
        "old": 0,                      # Mark this trial as a foil (0 = new, not previously seen)
        "stim": foil_stim})            # Store the PsychoPy ImageStim used to display this foil face

# Safety check: Confirming I have enough foils
    # I have 18 foils total (9 male, 9 female).
male_foils   = [f for f in foil_trials if f["gender"] == "male"]     # Create a list of only the male foil trials
female_foils = [f for f in foil_trials if f["gender"] == "female"]   # Create a list of only the female foil trials

if len(male_foils) < 9 or len(female_foils) < 9: # Check that there are at least 9 foils for each gender
    raise ValueError(  # Stop the experiment immediately if the foil set is incomplete
        f"Not enough foils found. Need at least 9 male + 9 female foils, "    # Explain the required number of foils
        f"but found {len(male_foils)} male and {len(female_foils)} female.")  # Report how many foils were actually found

# Randomize foils within each gender
rng.shuffle(male_foils)
rng.shuffle(female_foils)

# Select exactly 9 foils of each gender (18 total)
foil_trials = male_foils[:9] + female_foils[:9]

# Shuffle again so gender order is mixed
rng.shuffle(foil_trials)

# Combine OLD + FOILS and shuffle the memory list
memory_trials = old_trials + foil_trials
rng.shuffle(memory_trials)

    # This produces 54 total memory trials (36 old + 18 new).


# CREATING THE YES/NO BUTTON DISPLAY (RT IS NOT TRACKED)

memory_prompt = visual.TextStim( # Creating the text prompt to appear above each stim during the memory task
    win,
    text="Did you see this picture of this face?", # Same question I have used in all experiments 
    pos=(0, 260),
    color="black",
    font="Arial",
    bold=True,
    height=28)

memory_face = visual.ImageStim(  # This is a “placeholder” ImageStim that I re-use each trial.
                                 # Instead of creating a new ImageStim every time (inefficient), I just swap out the image.
    win,
    image=None,
    size=(240, 180),
    pos=(0, 80))

# COMMON BUTTON SETTINGS
    # Defining shared visual properties so YES and NO buttons stay identical
button_kwargs = dict(
    win=win,                  # PsychoPy window the buttons will appear in
    width=180,                # Width of each button rectangle (in pixels)
    height=80,                # Height of each button rectangle (in pixels)
    fillColor="lightgray",    # Light fill color so buttons stand out against white background
    lineColor="black")        # Black outline to clearly define button boundaries


# COMMON BUTTON TEXT SETTINGS
    # Defining shared text properties for the YES/NO labels
button_text_kwargs = dict(
    win=win,                  # PsychoPy window for text rendering
    color="black",            # Black text for readability
    font="Arial",             # Consistent font across the experiment
    bold=True,                # Bold text to make YES/NO visually salient
    height=26)                # Text size chosen to fit cleanly inside the buttons


# YES BUTTON
    # Rectangle that participants click to indicate "YES"
yes_button = visual.Rect(
    pos=(-140, -220),         # Position of the YES button on the left side of the screen
    **button_kwargs)          # Apply all shared button settings


# YES BUTTON TEXT
    # Text label centered inside the YES button
yes_text = visual.TextStim(
    text="YES",               # Label shown inside the button
    pos=(-140, -220),         # Same position as the button so text is centered
    **button_text_kwargs)     # Apply shared text formatting


# NO BUTTON
    # Rectangle that participants click to indicate "NO"
no_button = visual.Rect(
    pos=(140, -220),          # Position of the NO button on the right side of the screen
    **button_kwargs)          # Apply all shared button settings


# NO BUTTON TEXT
    # Text label centered inside the NO button
no_text = visual.TextStim(
    text="NO",                # Label shown inside the button
    pos=(140, -220),          # Same position as the button so text is centered
    **button_text_kwargs)     # Apply shared text formatting


mouse = event.Mouse(win=win)        # Creates a mouse object so we can detect clicks on the YES/NO buttons during the memory task
mouse.clickReset()                  # Clears any previous mouse clicks so the first memory trial does not accidentally register an old click

# RUNNING THE MEMORY TASK TRIAL LOOP

for mem_index, trial in enumerate(memory_trials, start=1):
    # Loops through each memory trial one at a time, giving each trial a number (starting at 1) and the corresponding face to be tested in memory

    memory_face.image = trial["stim"].image
        # Put the current face into the placeholder ImageStim

    responded = False  # Flag to track whether the participant has made a response on this memory trial
    while not responded:  # Keep looping until the participant clicks YES or NO

        memory_prompt.draw()  # Draws the memory question text at the top of the screen
        memory_face.draw()    # Draws the current face being tested for memory
        yes_button.draw(); yes_text.draw()  # Draws the YES button rectangle and its label
        no_button.draw();  no_text.draw()   # Draws the NO button rectangle and its label
        win.flip()  # Updates the screen so all drawn elements appear to the participant
            
        if mouse.isPressedIn(yes_button):   # Check whether the participant clicked inside the YES button
                                                # https://www.psychopy.org/api/event.html#psychopy.event.Mouse.isPressedIn
            response = 1                    # Code YES responses as 1
            responded = True                # Mark the trial as complete so we can exit the response loop
        elif mouse.isPressedIn(no_button):  # Check whether the participant clicked inside the NO button
            response = 0                    # Code NO responses as 0
            responded = True                # Mark the trial as complete so we can exit the response loop

        keys = event.getKeys()     # Check for any keyboard input (e.g., escape key)
        if "escape" in keys:       # Allow the experimenter to terminate the experiment early if needed
            csv_file.close()       # Close the CSV file safely so no data are lost
            core.quit()            # Exit PsychoPy and stop the experiment immediately


    correct = int(response == trial["old"])
        # Correct is computed as YES on old items OR NO on foil items
        # This is the trial-level accuracy score (good for computing hits/FA later).

    # Save MEMORY responses into the SAME CSV FILE
        # Grid columns are left blank here; memory columns are filled in.
    csv_writer.writerow({
        "task": "memory",
        "participant_index": participant_index,
        "subject_group": subject_group,
        "trial_index": mem_index,
        "datetime_local": datetime.now().isoformat(timespec="seconds"),

        # GRID columns left blank for memory rows
        "trial_gender_code": "",
        "trial_gender_label": "",
        "angry_estimate": "",
        "happy_estimate": "",
        "neutral_estimate": "",
        "total": "",
        "identities_shown": "",
        "emotions_shown": "",

        # MEMORY columns filled
        "memory_identity": trial["identity"],
        "memory_gender": trial["gender"],
        "memory_emotion": trial["emotion"],
        "old": trial["old"],
        "response": response,
        "correct": correct,

        # RATINGS columns left blank for memory rows
        "rating_identity": "",
        "rating_gender": "",
        "rating_emotion": "",
        "negativity_rating": ""})

    csv_file.flush() # https://docs.python.org/3/library/io.html#io.IOBase.flush
         # Make sure it writes immediately (so I don't lose data if it crashes later)
    mouse.clickReset()
        # Clears the click so the next trial does not instantly register the previous click again
    core.wait(0.2)
        # Short pause between trials to reduce accidental double-clicks and make the task feel smoother.

#-------------------------
# 5) EMOTION RATINGS TASK
#-------------------------

# This task comes AFTER memory so participants do not start thinking about "negativity" during the grid/memory judgments.
    # It shows ONLY the 36 OLD faces they saw in the grid task (no foils).

ratings_instructions = visual.TextStim(
    win,
    text=(
        "In this last portion of the study, you will rate each face on a 1 to 9 scale for how negative the face's emotion looks to you.\n\n"
        
        "Choosing \"1\" would mean that the face's emotion looked very positive, choosing \"5\" would mean the face's emotion look neutral, and choosing \"9\" would mean the face's emotion looked very negative.\n\n"
        
        "Use the rating scale under each face, then press SPACE to continue."
    ),
    color="black",
    wrapWidth=1000,
    font="Arial",
    height=28,
    bold=False)

ratings_instructions.draw()           # Draw the ratings instructions
win.flip()                            # Display them to the participant
event.waitKeys(keyList=["space"])     # Wait for SPACE before starting the ratings task
event.clearEvents()                   # Clear the key buffer so SPACE does not carry into the first rating trial

rating_trials = old_trials.copy()
    # Copying old_trials ensures we only rate faces that were actually shown in the grid task (the 36 OLD items).

rng.shuffle(rating_trials)
    # Randomize the order of rating trials so participants do not rate all angry/happy/neutral in a predictable block.

rating_prompt = visual.TextStim(
    win,
    text="How negative is this face on a 9-point scale?",
    pos=(0, 260),
    color="black",
    font="Arial",
    bold=True,
    height=28)

rating_face = visual.ImageStim(
    win,
    image=None,
    size=(240, 180),
    pos=(0, 80))
    # This is another reusable placeholder ImageStim (same idea as memory_face).

rating_ticks = list(range(1, 10))
    # Creates the 1–9 scale values.

rating_labels = [
    "Very\npositive" if t == 1 else
    "Neutral"       if t == 5 else
    "Very\nnegative" if t == 9 else
    ""
    for t in rating_ticks]
        # Only label the anchor points (1, 5, 9) so the screen stays clean.

negativity_slider = Slider(          # Create the 1–9 rating slider the participant will use for negativity ratings
    win=win,                         # Draw the slider in my existing PsychoPy window
    ticks=rating_ticks,              # The possible values on the scale (i.e., 1 through 9)
    labels=rating_labels,            # The text labels shown under ticks (only 1, 5, and 9 are labelled)
    granularity=1,                   # Force whole-number steps so ratings are integers (no decimals)
    size=(900, 60),                  # Make the slider wide enough to be easy to click and read
    pos=(0, -160),                   # Place the slider under the face stimulus on the screen
    labelHeight=26,                  # Set how big the tick labels appear (so anchors are readable)
    style=("rating"),                # Use PsychoPy's rating-style slider (looks like a rating scale)
    color="black",                   # Set the main slider elements to black for visibility on white background
    fillColor="red",                 # Color the filled portion to highlight the chosen rating
    markerColor="black",             # Make the marker/handle black so it stands out clearly
    lineColor="black",               # Ensure the slider track line is visible
    font="Arial")                    # Keeping font consistent with the rest of the experiment
    # A 1–9 slider where the participant chooses how negative the emotion looks.

ratings_backup = []
    # I am storing ratings in a Python list too (similar to grid_estimates) in case I ever wanted an in-script summary.

for rate_index, trial in enumerate(rating_trials, start=1):
    # Loop through all 36 OLD faces (one at a time), assigning a clean trial index for the ratings task.

    negativity_slider.reset()
        # reset() is important so each face starts with no rating selected (prevents carry-over from the previous face).

    event.clearEvents()
        # Clears held-down keys so a SPACE press from the last screen does not auto-advance.

    rating_face.image = trial["stim"].image
        # Put the current face into the rating placeholder ImageStim.

    while True:

        rating_prompt.draw()
        rating_face.draw()
        negativity_slider.draw()
        win.flip()
            # Draw the face + the rating scale underneath and update the screen.

        keys = event.getKeys()
        if "escape" in keys:
            csv_file.close()
            core.quit()
                # Emergency quit option (same logic as the other tasks).

        current_rating = negativity_slider.getRating()
            # getRating() returns None if the participant has not selected a value yet.

        if "space" in keys and current_rating is not None:
            # Only allow the participant to continue if they pressed SPACE AND they actually chose a rating.

            ratings_backup.append({
                "participant_index": participant_index,
                "subject_group": subject_group,
                "trial_index": rate_index,
                "identity": trial["identity"],
                "gender": trial["gender"],
                "emotion": trial["emotion"],
                "negativity_rating": int(current_rating)})
                # Backup list so the ratings are stored in Python too (not just the CSV).

            csv_writer.writerow({
                "task": "ratings",                                    # Marks this row as the ratings task
                "participant_index": participant_index,                # Participant #
                "subject_group": subject_group,                        # Subject group
                "trial_index": rate_index,                             # Ratings trial index (1–36)
                "datetime_local": datetime.now().isoformat(timespec="seconds"),  # Time rating was recorded

                "trial_gender_code": "",                               # Blank (only relevant for grid)
                "trial_gender_label": "",                              # Blank (only relevant for grid)
                "angry_estimate": "",                                  # Blank (only relevant for grid)
                "happy_estimate": "",                                  # Blank (only relevant for grid)
                "neutral_estimate": "",                                # Blank (only relevant for grid)
                "total": "",                                           # Blank (only relevant for grid)
                "identities_shown": "",                                # Blank (only relevant for grid)
                "emotions_shown": "",                                  # Blank (only relevant for grid)

                "memory_identity": "",                                 # Blank (only relevant for memory)
                "memory_gender": "",                                   # Blank (only relevant for memory)
                "memory_emotion": "",                                  # Blank (only relevant for memory)
                "old": "",                                             # Blank (only relevant for memory)
                "response": "",                                        # Blank (only relevant for memory)
                "correct": "",                                         # Blank (only relevant for memory)

                "rating_identity": trial["identity"],                  # Identity being rated (one of the OLD faces)
                "rating_gender": trial["gender"],                      # Gender of the rated face
                "rating_emotion": trial["emotion"],                    # Emotion version being rated (angry/happy/neutral)
                "negativity_rating": int(current_rating)})             # 1–9 negativity rating

            csv_file.flush()
                # Make sure it writes immediately (same safety logic as the other tasks).

            break
                # Exits the rating loop and moves on to the next face.

    core.wait(0.2)
        # Small pause so it feels less “clicky” between rating trials.

#----------------
# 6) END SCREEN
#----------------

end_screen = visual.TextStim(
    win,
    text="Great work! The experiment is now over.\n\nPress SPACE to exit.",
    color="black",
    wrapWidth=1000,
    font="Arial",
    height=32,
    bold=True)
    # End screen makes it clear to participants that they are done and prevents the window from just disappearing.

end_screen.draw()
win.flip()
event.waitKeys(keyList=["space"])
event.clearEvents()
    # Waiting for SPACE gives the participant control over when to finish (this is nice for in-lab setups).

# --------------
# A CLEAN CLOSE
# --------------

csv_file.close()
    # Closing the CSV at the very end ensures all three tasks have finished writing their rows.

core.quit()
    # Clean exit from PsychoPy.