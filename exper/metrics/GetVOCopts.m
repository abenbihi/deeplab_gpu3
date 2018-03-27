function VOCopts = GetVOCopts()
%clear VOCopts


data_root = '/home/gpu_user/AgroParisTech/data/new_dataset';
res_root_folder ='/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/' ;

data_dir='Data2015/'
xp_name = 'deeplab_bgr2015_sgd_crf/';

data_folder=fullfile(data_root, data_dir);
val_label_folder = fullfile(data_folder, 'Valid/Label');
list_folder = fullfile('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/list/', data_dir);
VOCopts.val_list = fullfile(list_folder, '/val_label_img.txt')

VOCopts.res_dir = fullfile(res_root_folder, xp_name, 'png_class/');

% classes
% old dataset
% don't put the background/mask class
VOCopts.classes={...
  '0'
  '1'
  '2'
  '3'
  '4'
  '5'
  '6'
  '7'
  '8'
  '9'
  '10'
  '11'
  '12'
  '13'};
  
 
VOCopts.nclasses=length(VOCopts.classes);	

