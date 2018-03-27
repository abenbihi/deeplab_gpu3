% convert the network output with crf outside network : bin 2 png

xp_name = 'deeplab_bgr2015_sgd_crf'

%map_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/bin/');
map_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/features/', xp_name);
fprintf(1,' from %s\n', map_folder);
map_dir = dir(fullfile(map_folder, '*.bin'));

save_result_color_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/png_color/');

save_result_class_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/', xp_name, '/png_class/');

if ~exist(save_result_class_folder, 'dir')
    mkdir(save_result_class_folder);
end

if ~exist(save_result_color_folder, 'dir')
    mkdir(save_result_color_folder);
end

%fprintf(1,' saving to %s\n', save_result_folder);
fprintf(1,' from %s\n', map_folder);
numel(map_dir)

for i = 1 : numel(map_dir)
    fprintf(1, 'processing %d (%d)...\n', i, numel(map_dir));
    map = LoadBinFile(fullfile(map_folder, map_dir(i).name), 'int16');

    img_fn = map_dir(i).name(1:end-4);
    imwrite(uint8(map), colormap, fullfile(save_result_color_folder, [img_fn, '.png']));
    imwrite(uint8(map), fullfile(save_result_class_folder, [img_fn, '.png']));
end
