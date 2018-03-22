

function [] = JpgToPPM(img_root_folder,save_root_folder)

files = dir(img_root_folder);
directoryNames = {files([files.isdir]).name};
directoryNames = directoryNames(~ismember(directoryNames,{'.','..'}));

for i=1:length(directoryNames)
    img_folder = fullfile(img_root_folder, directoryNames{i});
    save_folder = fullfile(save_root_folder, directoryNames{i});

    if ~exist(save_folder, 'dir')
        mkdir(save_folder);
    end
    
    img_dir = dir(fullfile(img_folder, '*.png'));
    
    for i = 1 : numel(img_dir)
        fprintf(1, 'processing %d (%d)...\n', i, numel(img_dir));
        img = imread(fullfile(img_folder, img_dir(i).name));
        
        img_fn = img_dir(i).name(1:end-4);
        save_fn = fullfile(save_folder, [img_fn, '.ppm']);
        
        imwrite(img, save_fn);   
    end
end
