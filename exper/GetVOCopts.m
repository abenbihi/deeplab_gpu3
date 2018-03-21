function VOCopts = GetVOCopts()
%clear VOCopts

% /home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set
% /home/gpu_user/AgroParisTech/data/new_dataset/Data2015
data_folder='/home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set/';

res_root_folder ='/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/' ;

xp_name = 'bgrir_sgd/';

val_rgb_folder = '';

val_label_folder = '/home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set/val_label/';
% /home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set/val_label
% /home/gpu_user/AgroParisTech/data/new_dataset/Data2015/Valid/Label

list_folder = '/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/list/';

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

