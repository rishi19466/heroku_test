import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import tensorflow
import cv2
import subprocess
import sys
import tensorflow_hub as hub

def install(package):
    subprocess.check_call([sys.executable,"-m","pip","install",package])

install('simplemma==0.5.0')

st.title('Safe/Unsafe Driving Prediction on the basis of Drivers Action')
st.markdown('This Project is built as part of University of Hyderabads Machine Learning and Applied AI course')
st.markdown('Built by Deepak Rawat- vagadro@gmail.com')

def main():
    file_uploaded=st.file_uploader("Upload the Image",type=['jpg','png','jpeg'])
    if file_uploaded is not None:
        image=Image.open(file_uploaded)
        figure=plt.figure()
        plt.imshow(image)
        plt.axis('off')
        result= predict_class(image)
        st.write(result)
        st.pyplot(figure)

def predict_class(image):
    classifier_model= tensorflow.keras.models.load_model('model_cnn.h5')
    shape=((64,64,3))
    model=tensorflow.keras.Sequential([hub.KerasLayer(classifier_model, input_shape=shape)])
    test_image=image.resize((64,64))
    test_image=tensorflow.keras.preprocessing.image.img_to_array(test_image)
    test_image=test_image/255.0
    test_image=np.expand_dims(test_image, axis=0)

#    test_image = cv2.resize(image, (64, 64))
#    test_input = test_image.reshape((1, 64, 64, 3))
    class_names = ["SAFE_DRIVING",
                   "TEXTING_RIGHT",
                   "TALKING_PHONE_RIGHT",
                   "TEXTING_LEFT",
                   "TALKING_PHONE_LEFT",
                   "OPERATING_RADIO",
                   "DRINKING",
                   "REACHING_BEHIND",
                   "HAIR_AND_MAKEUP",
                   "TALKING_TO_PASSENGER"
                   ]
    predictions = model.predict(test_image)
    scores = tensorflow.nn.softmax(predictions[0])
    scores = scores.numpy()
    image_class = class_names[np.argmax(scores)]
    result= "The Driver is: {}".format(image_class)
    return result

if __name__=='__main__':
    main()

