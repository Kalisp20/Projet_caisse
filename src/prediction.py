import numpy as np
import os
import time

import PIL.Image as Image
import matplotlib.pylab as plt

import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
class vision_pred(object):
   def prediction(product):
      model= tf.keras.models.load_model('src/saved_model/my_model/')
      
      class_names=['Abricot', 'Abricot-Sec', 'Ail', 'Ananas', 'Artichaut', 'Asperge',
         'Aubergine', 'Avocat', 'Banane', 'Bette', 'Betterave-Rouge',
         'Carambole', 'Carotte', 'Cassis', 'Cerise', 'CéLeri-Branche',
         'CéLeri-Rave', 'Chou', 'Chou-Fleur', 'Citron-Jaune',
         'CléMentine', 'Coing', 'Concombre', 'Courgette', 'Endive',
         'ÉChalote', 'Fenouil', 'Figue', 'Fraise', 'Framboise',
         'Gimgembre', 'Haricot-Vert', 'Igname', 'Kaki', 'Kiwi', 'Kumquate',
         'Laitue', 'Litchi', 'Mangue', 'Manioc', 'Melon', 'MûRe',
         'Myrtille', 'Navet', 'Nectarine', 'Noix-De-Coco', 'Oignon',
         'Orange', 'Papaye', 'PastèQue', 'Patate-Douce', 'PêChe', 'Poire',
         'Poireau', 'Poivron', 'Pomelos', 'Pomme', 'Pomme-De-Terre',
         'Potiron', 'Prune', 'Radis', 'Raisin', 'Rhubarbe', 'Taro',
         'Tomate']
      
      IMAGE_SHAPE = (224, 224)
      product = Image.open(product).resize(IMAGE_SHAPE)
      product = np.array(product)/255.0
      product.shape

      result = model.predict(product[np.newaxis, ...])
      result.shape

      predicted_class = np.argmax(result[0], axis=-1)
      predicted_class_name = class_names[predicted_class]

      return predicted_class_name.title()