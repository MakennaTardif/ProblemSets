# PSYC 5P02- Introduction to Programming for Psychology
## Fall 2025

### Problem Set #3

### Rubric:
* Accuracy & Efficiency: 50%
* Explanation and documentation: 50%

--- 
###  Feedback:
* I think we went through a sample example of how to use the dialogue box in the Psychopy lecture notes. It's just a few lines:
 > ``info = {'Participant': '', 'Trials per set size': ''} # creates a dictionary to store key experiment info``
 
 > ``dlg = gui.DlgFromDict(info, title='Input Experiment Details') # creates a dialog box based on the dictionary created above
if not dlg.OK:
    core.quit() # quits experiment if OK not clicked on dialog box ``
 
* You've hard-coded some stuff in a way that could lead to problems. For example you defined ``Num_Trials = 10 `` but then when creating your trial list you use ``trial_types = [1]*5 + [0]*5`` . Use ``Num_Trials/2`` instead of `5` as it's more flexible and the values are linked. 
* Using a dictionary and the .csv library seems like an effective way to save the data. **However**...I believe it is only writing after all trials are run. So if the experiment crashes or it ends before it's complete you don't have any data saved. The nice thing about the method I showed you in class is that it writes data on every trial. 
* You are re-using a lot of code for both the practice and experimental trials. Try to wrap repeated code into a function (def) or a class if possible.
* I appreciate the use of randomization but randomly pulling a set size or present/absent value may end up in uneven trial numbers, which could be a problem. 
* The use of the formatted strings works, and I appreciate the documentation, but you could also simply turn any variable into a string with ``str()`` and then concatenate them with other strings. Like: ``"Accuracy: " + str(accuracy)``
*  **Overall:** Generally speaking very good. Managed to accomplish most of what I asked. Shows good use of concepts. Some hard coding. Could be made more efficient with the use of functions or classes for repeated code. 

**Accuracy & Efficiency:** 18/25
**Explanation and documentation:** 25/25
**Total:** 43/50
