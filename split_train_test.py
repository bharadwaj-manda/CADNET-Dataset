import os, random, shutil


def split_train_test(dir, test_split=5):


    if not os.path.exists(dir):
        raise Exception("dir Not exist!")

    output_dir = dir + "_split_train_test"

    class_dir_list = os.listdir(dir)

    for class_dir in class_dir_list:
        class_dir_path = os.path.join(dir, class_dir)

        model_dir_list = os.listdir(class_dir_path)
        file_no = len(model_dir_list)
        test_file_no = file_no//test_split
        for _ in range(test_file_no):
            test_dir = random.choice(model_dir_list)
            model_dir_list.remove(test_dir)
            source_dir = os.path.join(class_dir_path, test_dir)
            destination_dir = os.path.join(output_dir, "test_dir", class_dir, test_dir)

            #print("source_dir: ", source_dir)
            #print("destination_dir: ", destination_dir)


            shutil.copytree(source_dir, destination_dir,  symlinks=True, ignore=None)

        for train_dir in model_dir_list:
            source_dir = os.path.join(class_dir_path, train_dir)
            destination_dir = os.path.join(output_dir, "train_dir", class_dir, train_dir)

            shutil.copytree(source_dir, destination_dir,  symlinks=False, ignore=None)


if __name__ == "__main__":
    split_train_test('/home/bharadwaj/Research/Classification/Data_lfd')
    # dir = 'Image_Folder'
    # for folder in os.listdir(dir):
    #     split_train_test(os.path.join(dir,folder))
