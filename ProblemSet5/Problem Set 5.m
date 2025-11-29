%% Question 1: Creating and Modifying Vectors

% This is the original vector of RTs provided, in milliseconds (ms)
RT = [520 498 601 1200 450 475 3000 510 490];  % Copy and pasted

% Here I am using logical indexing in order to remove any RTs greater than 1500 ms
RT_clean = RT(RT <= 1500);

% Next, I need to compute and display all of the required values
mean_RT = mean(RT_clean);  % Mean RT for the cleaned data (https://www.mathworks.com/help/matlab/ref/double.mean.html)
median_RT = median(RT_clean);  % Median RT for the cleaned data (https://www.mathworks.com/help/matlab/ref/double.median.html)
num_removed = length(RT) - length(RT_clean);   % Number of removed RT's

% Here, I am displaying/printing the results 
fprintf('Problem 1 Results:\n');  
fprintf('Mean RT: %.2f ms\n', mean_RT);   % Mean rt calculated above
fprintf('Median RT: %.2f ms\n', median_RT);  % Median RT calculated above
fprintf('Number of trials removed: %d\n', num_removed);  % Number of trials removed that I calculated above

% Note: There should only be 1 trial removed (i.e., there is only 1 trial over 1500 ms)

%% Question 2: Matrix Manipulation

% I need to create a 10 × 3 matrix called "data" representing 10 trials.

% Column 1: Stimulus intensity (i.e., random integers from 1–100)
stimIntensity = randi([1 100], 10, 1);  % Link: https://www.mathworks.com/help/matlab/ref/double.randi.html

% Column 2: Condition (1 = low load, 2 = high load), randomly assigned
condition = randi([1 2], 10, 1);

% Column 3: Response (random integers 1 or 2)
response = randi([1 2], 10, 1);

% Next I need to combine all three columns into ONE matrix
data = [stimIntensity condition response];  % Link: https://www.mathworks.com/help/matlab/math/creating-and-concatenating-matrices.html

% Now I need to extract all high-load trials into a new matrix "highLoadData"
highLoadData = data(data(:,2) == 2, :);  % Link: https://www.mathworks.com/help/matlab/math/array-indexing.html#btjg9qm-1

% Finally, I need to compute the mean stimulus intensity separately for each condition
meanIntensity_low  = mean(data(data(:,2) == 1, 1));
meanIntensity_high = mean(data(data(:,2) == 2, 1));

% Again, I should display the results  
% Link for this section: https://www.mathworks.com/help/matlab/ref/fprintf.html
fprintf('Problem 2 Results:\n');    
fprintf('  Mean intensity (low load):  %.2f\n', meanIntensity_low);  % Mean intensity for low load
fprintf('  Mean intensity (high load): %.2f\n\n', meanIntensity_high);  % Mean intensity for high load

%% Question 3: If Statements

% Given criterion from the question (copy and pasted)
criterion = 50;

% Using the data matrix from Problem 2:
% Column 1 = stimulus intensity
% Column 3 = participant response

fprintf('Problem 3 Results:\n');

for i = 1:size(data,1)     % For loop link: https://www.mathworks.com/help/matlab/ref/for.html
                           % Size link: https://www.mathworks.com/help/matlab/ref/size.html
    
    stimulus = data(i,1);
    response = data(i,3);

    % Determine the correct response based on the rules provided:
    % stimulus <  criterion → correct response = 1
    % stimulus >= criterion → correct response = 2
    if stimulus < criterion    % If/else link: https://www.mathworks.com/help/matlab/ref/if.html
        correctResponse = 1;
    else
        correctResponse = 2;
    end

    % Need to compare the participant's response to the correct response
    if response == correctResponse     % Link: https://www.mathworks.com/help/matlab/matlab_prog/array-comparison-with-relational-operators.html
        fprintf('Trial %d: Correct\n', i);
    else
        fprintf('Trial %d: Incorrect\n', i);
    end
end

fprintf('\n'); 

%% Question 4: While Loops

% The recursive function is in a separate .m file called "removeOutliers"

% First, I need to create the RTs: 
% i.e., 100 values, normally distributed around 700 m with up to 400 ms uniform noise added
RTs = 700 + randn(100,1)*70 + randi([0 400], 100, 1);   % Link: https://www.mathworks.com/help/matlab/ref/double.randn.html

% I need to call the recursive outlier-removal function
[cleanRTs, removedRTs, iterations] = removeOutliers(RTs);

% Computing the final cleaned mean
finalMean = mean(cleanRTs);

% The number of outliers removed
totalRemoved = length(removedRTs);  % Uses the length of the removed outliers 

% Printing the results using formatted text
fprintf('Problem 4 Results:\n');
fprintf('  Final cleaned mean RT: %.2f ms\n', finalMean);  % Printing cleaned mean RT calculated above
fprintf('  Number of iterations: %d\n', iterations);       % Printing how many iterations were done
fprintf('  Total outliers removed: %d\n\n', totalRemoved); % Printing how many outliers were actually removed

%% Question 5: Structures (Link: https://www.mathworks.com/help/matlab/matlab_prog/create-a-structure-array.html)

% First I need to load the file
load('experiment_data.mat');    % This loads the structure "data"

fprintf('Problem 5:\n');

fprintf('\nSubject 1:\n');

% Now I need to print the participant ID
fprintf('Participant ID: %s\n', data.participant);

% Next I need to display the number of trials recorded for that subject
nTrials = numel(data.trials);   % trials is a 1×10 struct array
fprintf('  Number of trials: %d\n', nTrials);

% I now need to compute the mean RT across all trials
% The RTs are stored in data.trials(i).rt
allRTs = [data.trials.rt];      % Making a numeric vector of RTs
data.mean_RT = mean(allRTs);
fprintf('  Mean RT: %.2f ms\n', data.mean_RT);  % Printing the mean RT

% I also need to compute the accuracy and add it to a field called accuracy
% Responses are stored in data.trials(i).response (e.g., 'yes' / 'no')
responses = {data.trials.response};          % 1×10 cell array of chars
isCorrect = strcmp(responses, 'yes');        % logical vector
data.accuracy = mean(isCorrect);             % the proportion correct
fprintf('  Accuracy: %.2f\n', data.accuracy);

% Next I need to create a NEW subject with 10 RTs (using DEAL as the hint suggests)

% I need to start by copying the first subject so the fields actually exist
data(2) = data(1);

% Now I need to give the new subject a different participant ID
data(2).participant = 'P002';  % Similar structure to participant 1 (P001)

% Next I need to create 10 new RTs (example: around 700 ms with some noise)
newRTs = 700 + randn(1,10)*50;   % 1×10 double
newRTsCell = num2cell(newRTs);   % Converting to 1×10 cell for DEAL function

% I also need to create 10 new responses (Example: mostly 'yes', few 'no')
newResponses = repmat({'yes'}, 1, 10);   % start with all correct
newResponses(randperm(10, 2)) = {'no'};  % randomly make 2 incorrect

% Now I need to use DEAL to assign rt and response into the 1×10 trials struct
[data(2).trials.rt]       = deal(newRTsCell{:});    % Link: https://www.mathworks.com/help/matlab/ref/deal.html
[data(2).trials.response] = deal(newResponses{:});

% Must keep the same conditions as subject 1
% (This is already true because I copied data(1) into data(2) above,
% so I don't actually need to change the condition field here.)

% Finally, I need to compute the new subject summary fields
allRTs2      = [data(2).trials.rt];                 % RTs for subject 2
responses2   = {data(2).trials.response};           % responses for subject 2
isCorrect2   = strcmp(responses2, 'yes');           % correct = 'yes'
data(2).mean_RT  = mean(allRTs2);                   % subject 2's mean RT
data(2).accuracy = mean(isCorrect2);                % subject 2's mean accuracy

% Now I want to print a summary for subject 2
fprintf('\nSubject 2:\n');   % Link: https://www.mathworks.com/help/matlab/ref/double.numel.html 
                             % Numel - Prints the number of elements in an array 
                             % One iteration per subject
fprintf('  Participant ID: %s\n', data(2).participant);
fprintf('  Number of trials: %d\n', numel(data(2).trials));
fprintf('  Mean RT: %.2f ms\n', data(2).mean_RT);
fprintf('  Accuracy: %.2f\n', data(2).accuracy);

%% Optional bonus: Plotting RTs after each iteration of the recursive function

% Reference link: https://www.mathworks.com/help/matlab/ref/plot.html

% This section reproduces the recursion externally for visualization
% I wanted to avoid chnanging the original function as it did not give me the RTs from each intermediate iteration
% I likely would have needed the function to also return the intermediate RT array

RTs_temp = RTs;            % Coping the original RTs (Because I do not want to change the original)
iteration = 0;

figure;                    % Opening a new figure for plotting

while true
    iteration = iteration + 1;  % Increases the iteration counter by one each time the loop runs
                                % To keep track of how many outlier-removal cycles have been completed.

    mu = mean(RTs_temp);  
    sd = std(RTs_temp);   % Link: https://www.mathworks.com/help/matlab/ref/double.std.html

    % Identify the outliers (same rule as removeOutliers)
    outliers = (RTs_temp < mu - 2*sd) | (RTs_temp > mu + 2*sd);

    % Stop if no outliers left
    if ~any(outliers)   % If there is not outliers, stop/break
        break;
    end

    % Remove the outliers
    RTs_temp = RTs_temp(~outliers);

    % Plot after this iteration (The iteration # depends on the random data)
    clf;                                % Clear figure for next plot
    plot(RTs_temp, 'o');                 % Scatter-style plot
    title(sprintf('RTs After Iteration %d', iteration));
    xlabel('Trial Index');
    ylabel('RT (ms)');
    grid on;
    drawnow;                             % Force update immediately
end

%% Saving one .mat file

save('ProblemSet5_results.mat');
