function [ outputData ] = lowPassFilter( sampleRate, cutoffFeq, inputData )
%lowPassFilter Summary of this function goes here
%   Detailed explanation goes here
% sigma1 = sampleRate / 2 / pi / cutoff;
sigma = sampleRate / 2 / pi / cutoffFeq;
delta_t = 1 / sampleRate;
[lengthSignal, nPts] = size(inputData);
t = delta_t:delta_t:lengthSignal * delta_t;

rGaussian = 6;
window = -rGaussian * delta_t:delta_t:rGaussian * delta_t;
gFilter = normpdf(window, 0, sigma);
gFilter = gFilter / sum(gFilter);
gFilter = gFilter';

head = inputData(1:rGaussian,:);
tail = inputData(end - rGaussian + 1:end,:);
mirrorhead = flipud(head);
mirrortail = flipud(tail);
mirrorinput = [mirrorhead; inputData; mirrortail];
% for i = 1:nPts
outputData = conv2(mirrorinput, gFilter, 'same');
outputData = outputData(rGaussian + 1 : end - rGaussian,:);

% plot(t,inputData,'r');
% hold on;
% plot(t,outputData,'b');
fileID = fopen('data.txt','w');
unit = '%0.2f ';
formatSpec = unit;
for i = 2:nPts
	formatSpec = [formatSpec unit];
end
formatSpec = [formatSpec '\n'];
fprintf(fileID,formatSpec,outputData');
fclose(fileID);
end

