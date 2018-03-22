
import sys

if __name__=='__main__':

    if len(sys.argv)!=3:
        print("Bad number of arguments")
        exit(1)

    val_filename = sys.argv[1]
    val_id_filename = sys.argv[2]

    fval = open(val_filename)
    fval_id = open(val_id_filename,'w')

    for l in fval:
        full_img_name = l.split()[0] 
        img_name = full_img_name.split("/")[-1]
        img_id = img_name.split(".")[0]

        find = img_id.find("0")
        while find == 0 and len(img_id)>1:
            img_id = img_id[1:]
            find = img_id.find("0")

        fval_id.write(str(img_id) + "\n")

    fval.close()
    fval_id.close()
        
    
