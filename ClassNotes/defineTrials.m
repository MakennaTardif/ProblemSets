function [nTrials stimType] = defineTrials(subject, condition)
%%

if (subject == 999) | (condition == 0)
    nTrials = 10;
    stimType = 0;
    return;   %end the function early. Not a great piece of code here...
               ...because could have used an else-if statement instead
end                   
nTrials = 100;
stimType(1:nTrials./2) = 1;
stimType(nTrials./2 + 1:max(nTrials))=2;
uselessVariable = 100 * 100;  % local to the function (did not ask to return)
end 

[trials, stim] = defineTrials(999, 0)

defineTrials(100,2) % defaults to the first of the two variables 

