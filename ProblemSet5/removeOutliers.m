function [cleanRTs, removedRTs, iterations] = removeOutliers(RTs)
% removeOutliers - This recursively removes RT outliers beyond +/- 2 SD.
%
%   [cleanRTs, removedRTs, iterations] = removeOutliers(RTs)
%
%   INPUT variable:
%       RTs - a vector of reaction times
%
%   OUTPUT variables:
%       cleanRTs   - The final vector after all of the outliers are removed
%       removedRTs - All of the removed values (stacked across iterations)
%       iterations - The number of recursive passes performed on the data
%
%   This function continues to remove outliers until no more values exceed mean +/- 2 SD.

cleanRTs = RTs;
removedRTs = [];
iterations = 0;

while true
    mu = mean(cleanRTs);
    sd = std(cleanRTs);

    % Logical mask for outliers
    outliers = (cleanRTs < mu - 2*sd) | (cleanRTs > mu + 2*sd);

    if ~any(outliers)
        % No more outliers → stop
        break;
    end

    % Store removed values (i.e., all outliers)
    removedRTs = [removedRTs; cleanRTs(outliers)];

    % Keep all non-outliers (i.e., data without outliers)
    cleanRTs = cleanRTs(~outliers);

    iterations = iterations + 1;
end

end
