import streamlit as st
from stegano import lsb
import os
import numpy as np
from PIL import Image
import random
from skimage.metrics import structural_similarity as ssim


def upload():
    img = st.file_uploader("Upload an image file", type=["jpg", "png", "jpeg"])
    return img

def txt():
    text = st.text_input("Encoding text")
    return text

def enc(img,text):
    
    img_jpeg= Image.open(img)
    encode=lsb.hide(img_jpeg,text)
    return encode

def save(encode):
    if not os.path.exists("img_encoded"):
        os.mkdir("img_encoded")
    sav = os.path.join("img_encoded",str(random.randint(1,100))+".png")
    encode.save(sav)
    return sav

def open_saved(sav):
    img = Image.open(sav)
    return img

def display(img1,img2):
    st.write("Original image")
    st.image(img1,use_column_width=True)
    st.write("Encoded image")
    st.image(img2,use_column_width=True)

def SSIM(img1,img2):
    img1 = Image.open(img1)
    img1 = np.array(img1)
    img2 = np.array(img2)
    st.write("SSIM difference")
    SSIM = ssim(img1,img2, multichannel=True)
    st.write("SSIM: ",SSIM)
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1] * img1.shape[2])
    st.write("MSE: ",err)

def decod(img):
    decode = lsb.reveal(img)
    st.write("Decoded text: ",decode)

def delete():
    for file in os.listdir("img_encoded"):
        os.remove(os.path.join("img_encoded",file))

def main():
    img1 = upload()
    if img1:
        text = txt()
        if text:
            encode = enc(img1,text)
            sav = save(encode)
            img2 = open_saved(sav)
            if st.button("Display Images"):
                display(img1,img2)
                SSIM(img1,img2)
            if st.button("Decode Message"):
                    decod(img2)


if __name__ == "__main__":
    main()
    delete()