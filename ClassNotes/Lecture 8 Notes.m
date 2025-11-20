% for single line comments and % {%} for multiline comments

a = [1, 2, 3, 4, 5];
b = [1 2 3 4 5];

% clc clears the command window
% clear makes everything disappear (all variables go bye bye)
% clear (insert variable name) - Delete a specific variable, but not all

%%

% this is a new section (runs only in this section)

c= 1 + 1

%%

% who = what are your variables

% whos - gives you more info about each variable

%%

% commas separate out the columns 
% semi colons separate out the rows

% Row by column structure

%%

m = [1 2; 3 4; 5 6;]

% Creates a row by column matrix (example above is a 3 by 2)
% Needs to be rectangular (needs an element in every location in a rect)
% Matrix can also have non-numbers (see example below)

m = [1 2; NaN 4; 5 NaN] 

%%

% Indexing (round brackets)

a(3)

m(3,1) 

% Gives 5 because it goes down rows and then to the next column

%%

% Indexing

m([1,3]),1  % First column - The first and third rows 
m(:,2) % second columm and all rows 
m(2:3,2) % second column and 2 to 3
m(2:end,2) % second column (2 to the end)
A = 1:2:10 % start, step, end

%%

% More matrix stuff

a' % Takes the row and column vectors and flips them

% Helpful if data is in different shapes and you want them back together

%%

% Combining variables 

c = [a b]

%%

% Adding and deleting

c(12) = 6 

c(11) = []

%%

why % Does something funny

%%

% Rotating and transposing do different things '

a' 
rot90(a)

%%

% Multiplication & division - automatically for matrix
% Element-wise multiplication
d = a .* b;
% Element-wise division
e = a ./ b;

%%

save('myFirstMat')
clear % clears all variables/workspace
load myFirstMat.mat  % Reloads everything

%%

% Help functions

% You type help and then the name of the function without brackets

%%

% Calculations

% mean, min, max, std, etc
% No special libraries required (examples below)

mean(a)
mean(a')
mean(a, "all")
%%

% Random 

% Examples: rand(x), rand(m,n), randi(nmax,m,n), randn(m,n) 

% Defualt random number generator every time (rng('shuffle')  - to reset)

% You can seed random numbers to a particular value (rng(10);)

% Current state (variable = rng()) 
