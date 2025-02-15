import cv2 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from board import blankBoard , drawBoard , cut_chessboard
import os
import image_slicer



def predictboard(filepath, filename):
    img_width, img_height = 42, 42
    nb_validation_samples = 225
    batch_size = 132
    boardSize = 15
    tiles = image_slicer.slice(filepath, 225, save=False)
    image_slicer.save_tiles(tiles, directory='C:\\Users\\Karl\\Desktop\\UT\\CNN\\Data\\Test\\Black', prefix='image', format='jpeg')


    test_datagen = ImageDataGenerator(rescale=1. / 255)
    validation_data_dir = 'C:\\Users\\Karl\\Desktop\\UT\\CNN\\Data\\Test'
    validation_generator = test_datagen.flow_from_directory(
        directory = validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        shuffle=False,
        class_mode=None)
    validation_generator.reset()


    model = tf.keras.models.load_model('C:\\Users\\Karl\\Desktop\\UT\\CNN\\model.h5')
    pred = model.predict(validation_generator)
    predicted_class_indices=np.argmax(pred,axis=1)
    labels=(validation_generator.class_indices)
    labels2=dict((v,k) for k,v in labels.items())
    predictions=[labels2[k] for k in predicted_class_indices]
    print(labels)
    output = np.array(predicted_class_indices).reshape(-1,15)
    print(output)
    board = cv2.rotate(drawBoard(output), cv2.cv2.ROTATE_90_CLOCKWISE)
    board = cv2.flip(board, 1)
    path = 'C:\\Users\\Karl\\Desktop\\UT\\images\\Nchess\\'
    cv2.imwrite(os.path.join(path, filename + '.jpg'), cv2.flip(cv2.rotate(drawBoard(output), cv2.cv2.ROTATE_90_CLOCKWISE),1))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


folder = ('C:\\Users\\Karl\\Desktop\\UT\\neural-chessboard\\test\\out\\')

for filename in os.listdir(folder):
    print(filename)
    img = os.path.join(folder,filename)
    predictboard(img, filename)

