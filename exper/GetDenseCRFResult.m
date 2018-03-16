% compute the densecrf result (.bin) to png
%


map_folder = '/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/features/antoine/val/fc8/20/post_densecrf_W4_XStd49_RStd5_PosW3_PosXStd3/';
fprintf(1,' from %s\n', map_folder);
map_dir = dir(fullfile(map_folder, '*.bin'));

save_result_folder = './result';
if ~exist(save_result_folder, 'dir')
    mkdir(save_result_folder);
end
fprintf(1,' saving to %s\n', save_result_folder);
fprintf(1,' from %s\n', map_folder);
numel(map_dir)

for i = 1 : numel(map_dir)
    fprintf(1, 'processing %d (%d)...\n', i, numel(map_dir));
    map = LoadBinFile(fullfile(map_folder, map_dir(i).name), 'int16');

    img_fn = map_dir(i).name(1:end-4);
    imwrite(uint8(map), colormap, fullfile(save_result_folder, [img_fn, '.png']));
end
