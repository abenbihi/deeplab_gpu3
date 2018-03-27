SetupEnv;

VOCopts = GetVOCopts();

% get iou score
if strcmp(testset, 'val')
  [accuracies, avacc, conf, rawcounts] = MyVOCevalseg(VOCopts, id);
else
  fprintf(1, 'This is test set. No evaluation. Just saved as png\n');
end 

    
    

