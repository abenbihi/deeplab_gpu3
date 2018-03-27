% convert the network output with crf within network : bin 2 png

xp_name = 'deeplab_bgr2015_sgd_crf'

map_folder =fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/bin') 
fprintf(1,' from %s\n', map_folder);
map_dir = dir(fullfile(map_folder, '*0.mat'));

save_result_color_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/png_color');
if ~exist(save_result_color_folder, 'dir')
    mkdir(save_result_color_folder);
end

save_result_class_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/png_class/');
if ~exist(save_result_class_folder, 'dir')
    mkdir(save_result_class_folder);
end

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

    img_fn = map_dir(i).name(1:end-11);
    imwrite(uint8(map.data(1:300, 1:300)), colormap, fullfile(save_result_color_folder, [img_fn, '.png']));
    imwrite(uint8(map.data(1:300, 1:300)), fullfile(save_result_class_folder, [img_fn, '.png']));
end
