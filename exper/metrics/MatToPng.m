% compute the densecrf result (.bin) to png
%

%set(gca,'YDir','reverse')

map_folder = '/home/gpu_user/assia/ws/tf/deeplab/exper/blob0/' 
fprintf(1,' from %s\n', map_folder);
map_dir = dir(fullfile(map_folder, '*0.mat'));

save_result_folder = './blob0_png/';
if ~exist(save_result_folder, 'dir')
    mkdir(save_result_folder);
end

fprintf(1,' saving to %s\n', save_result_folder);
fprintf(1,' from %s\n', map_folder);
numel(map_dir)

for i = 1 : numel(map_dir)
    fprintf(1, 'processing %d (%d)...\n', i, numel(map_dir));
    map = load(fullfile(map_folder, map_dir(i).name));
    map.data = imrotate(map.data, 90);
    map.data = map.data(end:-1:1,:,:); % vertical flip
    % I4 = I(end:-1:1,end:-1:1,:); % vertical and horizontal flip
    % I2 = I(:,end:-1:1,:); % horizontal flip
    %map.data = map.data(:,end:-1:1,:);

    img_fn = map_dir(i).name(1:end-4);
    imwrite(uint8(map.data), colormap, fullfile(save_result_folder, [img_fn, '.png']));
end
