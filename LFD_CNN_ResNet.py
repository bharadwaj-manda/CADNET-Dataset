# Importing the Keras libraries and packages

from keras.callbacks import TensorBoard, ModelCheckpoint
from sklearn.metrics import confusion_matrix
from trainingplot import TrainingPlot

import time
import numpy as np
import pickle
import os
from math import ceil

# Data Prepossessing

from keras.preprocessing.image import ImageDataGenerator

def network():

    train_folder = '/home/bharadwaj/Research/Classification/Data_lfd_split_train_test/train_dir'
    test_folder = '/home/bharadwaj/Research/Classification/Data_lfd_split_train_test/test_dir'
    target_size = (256, 256)
    batch_size = 20
    np_epochs = 100
    dropout = 0.2

    train_datagen = ImageDataGenerator(rescale=1./ 255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./ 255)

    training_set = train_datagen.flow_from_directory(train_folder,
                                                     color_mode='grayscale',
                                                     target_size=target_size,
                                                     batch_size=batch_size,
                                                     class_mode="categorical")

    test_set = test_datagen.flow_from_directory(test_folder,
                                                color_mode='grayscale',
                                                target_size=target_size,
                                                batch_size=1,
                                                class_mode="categorical")

    steps_per_epoch = ceil(training_set.samples/batch_size)

    # Optimise the class weight because of class imbalance
    from sklearn.utils import class_weight
    class_weights = class_weight.compute_class_weight('balanced',
                                                      np.unique(training_set.classes),
                                                      training_set.classes)

    # Initialising the CNN
    from keras.models import Model,Input
    from keras.optimizers import Adam
    from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,\
        AveragePooling2D, Dropout, BatchNormalization, Activation, add
    from keras import metrics


    def Unit(x,filters,pool=False):
        res = x
        if pool:
            x = MaxPooling2D(pool_size=(2, 2))(x)
            res = Conv2D(filters=filters, kernel_size=[1, 1], strides=(2, 2), padding="same")(res)
        out = BatchNormalization()(x)
        out = Activation("relu")(out)
        out = Conv2D(filters=filters, kernel_size=[3, 3], strides=[1, 1], padding="same")(out)

        out = BatchNormalization()(out)
        out = Activation("relu")(out)
        out = Conv2D(filters=filters, kernel_size=[3, 3], strides=[1, 1], padding="same")(out)

        out = add([res, out])

        return out


    def model_v3():
        images = Input((256, 256, 1))

        net = Conv2D(32, (7, 7), activation='relu',padding="same")(images)

        # TODO: check the accuracy with net = Conv2D(64, (7, 7), activation='relu',padding="same")(images) and coment out next three 32 lines

        net = Unit(net,32)
        net = Unit(net,32)
        net = Unit(net,32)

        net = Unit(net,64,pool=True)
        net = Unit(net,64)
        net = Unit(net,64)

        net = Unit(net,128,pool=True)
        net = Unit(net,128)
        net = Unit(net,128)

        net = Unit(net, 256,pool=True)
        net = Unit(net, 256)
        net = Unit(net, 256)

        net = Unit(net, 512, pool=True)
        net = Unit(net, 512)
        net = Unit(net, 512)

        net = BatchNormalization()(net)
        net = Activation("relu")(net)
        net = Dropout(0.25)(net)

        net = AveragePooling2D(pool_size=(4,4))(net)
        net = Flatten()(net)
        net = Dense(units=512,activation="relu")(net)
        net = Dense(units=512, activation="relu")(net)
        net = Dense(units=test_set.num_classes, activation="softmax")(net)

        model = Model(inputs=images,outputs=net)

        return model

    model = model_v3()

    model.summary()

    model.compile(optimizer=Adam(0.001),loss="categorical_crossentropy",metrics=['acc', metrics.mae])

    # Time the network modul
    def printTime(start):
        end = time.time()
        duration = end - start
        if duration < 60:
            return "used: " + str(round(duration, 2)) + "s."
        else:
            mins = int(duration / 60)
            secs = round(duration % 60, 2)
            if mins < 60:
                return "used: " + str(mins) + "m " + str(secs) + "s."
            else:
                hours = int(duration / 3600)
                mins = mins % 60
                return "used: " + str(hours) + "h " + str(mins) + "m " + str(secs) + "s."

    set_time = time.time()
    plot_dir = f'Plot/{set_time}/'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    WEIGHT_FOLDER_NAME = f"weights/{set_time}/"
    if not os.path.exists(WEIGHT_FOLDER_NAME):
        os.makedirs(WEIGHT_FOLDER_NAME)

    # serialize model to JSON
    model_json = model.to_json()
    with open(WEIGHT_FOLDER_NAME+ str(time.time()) + ".json", "w") as json_file:
        json_file.write(model_json)


    plot_losses = TrainingPlot(filename=plot_dir + str(np_epochs) + '.jpg')
    tensorboard = TensorBoard(log_dir='TFlogs/CADNET_LFD_Logs/{}'.format(time.time()))
    checkpoint = ModelCheckpoint(WEIGHT_FOLDER_NAME + "{epoch:02d}-{val_acc:.2f}.model", monitor='val_acc',
                                 verbose=1, save_best_only=True, mode='max') # saves only the best ones

    start = time.time()

    history = model.fit_generator(training_set,
                                   steps_per_epoch=steps_per_epoch,
                                  epochs=np_epochs,
                                   validation_data=test_set,
                                  validation_steps=test_set.samples,
                                   class_weight=class_weights,
                                   callbacks=[tensorboard, checkpoint],
                                   verbose=1)

    training_time = printTime(start)


    [Loss ,Accuracy, Mean_square_error] = model.evaluate_generator(test_set, steps=len(test_set))




network()


    # prob = model.predict_generator(test_set)
    # predictions = np.argmax(prob, axis=-1)
    # label_map = (training_set.class_indices)
    # label_map = dict((v, k) for k, v in label_map.items())  # flip k,v
    # predictions_result = [label_map[k] for k in predictions]
    #
    # Confusion_Matrix = confusion_matrix(test_set.classes, predictions)
    #
    # print("%s: %.2f%%" % (model.metrics_names[1], Accuracy))
    # print(Confusion_Matrix)
