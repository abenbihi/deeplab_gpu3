import os

dirname = '/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/res/bgrir_sgd/png_class/63000/'
for f in os.listdir(dirname):
    print("f: ", f)
    f_new = "00000" + f
    f_full_path = os.path.join(dirname, f)
    new_name = os.path.join(dirname, f_new)
    os.rename(f_full_path, new_name)

    print("f_full_path: ", f_full_path)

