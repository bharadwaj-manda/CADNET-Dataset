# CADNET_Dataset

This is the repository for the 'CADNET' Dataset, associated with the paper ["A Convolutional Neural Network Approach to the Classification of Engineering Models"](https://ieeexplore.ieee.org/document/9343314). For further details, contact Bharadwaj Manda via [here](https://www.linkedin.com/in/bharadwaj-manda-9730ab114/) or [here](bharadwaj-manda.github.io/)

Please visit https://bharadwaj-manda.github.io/CADNET-Dataset/ for more details.

## LICENSE

This dataset is licensed under CC BY-NC-SA: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
This license is one of the Creative Commons licenses and allows users to share the dataset only if they (1) give credit to the copyright holder, (2) do not use the dataset for any commercial purposes, and (3) distribute any additions, transformations or changes to the dataset under this same license.

## Download

Download the Dataset [here](https://drive.google.com/file/d/1JpYHRy2hgOL1X1z9HNIcHv7v-PSJqxaC/view?usp=sharing)

## How to use this repository

These steps will help you implement the paper. Follow the steps given below in the exact same sequence

1. Download the CADNET dataset (zip file) from the link provided above

2. Extract the contents of the zip file. You should see a folder named CADNET_3317. This contains 43 categories of 3D CAD models (stl files).

3. Now download all the Python scripts provided in the repo and store them in the same directory as the CADNET_3317 folder.

4. Run the 'File_Searcher.py' - This generate a 'file_list.txt' containing paths to all the stl files.

5. Run the 'Mesh_to_Image.py' - This will generate a folder 'Data_lfd' containg all the 20 view images of each CAD model

6. Run the 'split_train_test.py' - to split the lfd folder into train and test split sets.

7. Now that the data pre-processing is done, you can go ahead and run the 'LFD_CNN_ResNet.py' and train the NeuralNet

## To cite this Dataset or Paper:

- Use the bibtex below:

```bibtex
@ARTICLE{9343314,  
author={Manda, Bharadwaj and Bhaskare, Pranjal and Muthuganapathy, Ramanathan},  
journal={IEEE Access},   
title={A Convolutional Neural Network Approach to the Classification of Engineering Models},   
year={2021},  
volume={9},  
number={},  
pages={22711-22723},  
doi={10.1109/ACCESS.2021.3055826}}
```

- Or use the plain text below

---

B. Manda, P. Bhaskare and R. Muthuganapathy, "A Convolutional Neural Network Approach to the Classification of Engineering Models," in IEEE Access, vol. 9, pp. 22711-22723, 2021, doi: 10.1109/ACCESS.2021.3055826.

---

*Thanks are due to the many members who have contributed 3D CAD models to the CADNET dataset.*
