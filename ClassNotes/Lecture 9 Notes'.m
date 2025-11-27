%% Logical operations

% ==, :>, >, <, >=, <=,|, &

1 == 0

%% If Statements

% Matlab does not care about indentation and spacing
% Need to start with if - and with end;

rng('shuffle');

a = rand();
myVar = 1==1;

if a < 0.3  % if the value a is less than .33 (if it returns true)
    b = a.^2;  %square
elseif a >= 0.33 && a <= .66    
    another = true;
    b = 0;
else % if everything returned false
    b = a.^.5; % squareroot
end; % this is the end of my first if statment

%% Switch/case

k = randi(6); % make a variable called k

switch k  % this is the start of switch
    case {1,2}
        VWMCapacity = 'low';
    case {3,4}
        VWMCapacity = 'med';
    otherwise
        VWMCapacity = 'high';  
    
end % end of switch

%% For Loops

% Identical to what we learned before but we need the end;

var = 11:21 % create a vector

for i = 1:length(var) % loop through elements of that vector (through range of vector)
    
    i
    var(i)
    a = var(i)^2
    
end % This is the end of the loop

%% Comparing indexing to loops

% tic/toc records how long it takes to evaluate

tic % start the clock
a = zeros(1,10); % this is pre-allocating a variable
toc % the end of the clock

b = []; % creating an empty variable
tic
for i = 1:10
    b(i) = i^2; % adding elements to b
end 
toc

tic
for i = 1:10
    a(i) = i^2; % inserting elements into the pre-allocated variable
end
toc

%% Embedding while loops

% Runs until a condition is false (as we learned before)
% Messy because it doesn't require indentation, but it is encouraged
% If you click an "if" it will so you the corresponding end
% Highlight everything - editor - indent 
% Take notes where the code/loop ends and starts

numLoops = 0;
a = 0;        % give it a start value
numLoops2 = 0;
numLoops3 = 0;
while a < .9    % make it meet some condition
    numLoops = numLoops + 1;
    a = rand();  % reset value of a
    if a < .5
        numLoops2 = numLoops2 + 1;
        if a < .1
            continue;
            numLoops3 = numLoops3 + 1;
        end % who do these belong to?
    end
    if a == .7    % here's an if statement that will break out of the loop
        break;
    end % who do these belong to??
end

%% Indexing 

% Easiest way to avoid looping is to use conditionals
% To automatically find/index the locations of certain values

x = round(10 + randn(100,1));  % random 100 normal numbers centered on 10

(x==10)
x(x==10)   % Where x is equal to 10 in variable x (returns all 10s)
find(x==10) 

%any and all

any(x==10)   % are any equal to 10? 

all(x==10)   % returns if all are equal to 10

%% Functions

% nargin - optional arguments 
function myfcn(arg1,arg2,arg3)
if nargin < 3
    arg3 = some_value;
end;
if nargin < 2
    arg2 = some_other_value;
end;
end;

subjectNum = input('Please enter the subject number: ');

%% Text

% Comparing strings:
'apples' == 'oranges'
strcmp('apples', 'oranges')

% You can ignore case with strcmpi

% String find:

strfind('where in the world is carmen sandiego', 'carmen sandiego')

% String replace:

strrep('a a a a ', ' ', [])


% Writing text to a file: 

fid = fopen('myFile.txt', 'wt');  % Open a file first (name and writing)
rr = 1.1:5.1;

fprintf(fid,'%3.2f\t',rr); % which file with the ID, format of text, 
fprintf(fid,'\n');
fprintf(fid,'%3.2f\t',rr + 2);

fclose(fid);

% Formatting text: With sprintf

name = ('what is your name?')
greeting = sprintf ('Hello, %s, welcome to your program.', name)

%% Cells

% use curly brackets now

cell1 = {'apples', 'oranges'}   % 1 by 2 cell (not a character or string)(looks like a spreadsheet)

cell1{1} % indexing (returns apples)

cell2 = {[1 2 3 4 5], [1 2 3 4 5 6]}  

cell2{1}(5) % You can index within an array in a cell

%% Structures

% Like cells, but are named variables in each element (like a dictionary)
% Nested variables (can keep nesting)

data.subject = "SME"

data.rt = [0.9, 1.2]

data(:).subject  % Vectorize them as well (this will return all subjects)

%% Datasets

% Make data function like excell sheets or delimited files 










