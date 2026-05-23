import streamlit as st
import cv2
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

st.title("Image Captioning In Live Camera With AI Trained Model")
# we create the indentifier
if "stop" not in st.session_state:
    st.session_state.stop=None
if "flag" not in st.session_state:
    st.session_state.flag=False
# Load model only once
@st.cache_resource
# In this mathod we load the pre-trained model of caption generation from image 
def load_model():
    processor=BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model=BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base",
        use_safetensors=True
    )
    return processor, model
# Give the processor or model from pre-trained model
processor, model = load_model()
st.subheader("Capture an image using your camera")
cam=cv2.VideoCapture(0)
frame_placeholder=st.empty()
if not cam.isOpened():
    st.error("Could not open webcam")
    st.stop()

# create the frame to catch for caption
_,frame=cam.read()  
frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

col1,col2=st.columns(2)
with col1:
    if st.button('Start/Restart'):
        st.session_state.stop=False
        st.session_state.flag=True
with col2:
    if st.button('Take image'):
        frame_placeholder.image(frame,caption="Captured Image",use_container_width=True)
        if(st.session_state.flag is True and st.session_state.stop is False):
            st.session_state.stop=True
            image=Image.fromarray(frame)
        with st.spinner("Generating Caption..."):
            inputs = processor(image,return_tensors="pt")

            output = model.generate(**inputs,max_length=30)

            caption = processor.decode(output[0],skip_special_tokens=True)
        st.subheader("Caption")
        st.success(caption)

# This is use present the camera view to the user to stop at one frame
while st.session_state.stop is False:
    success,frame=cam.read()
    if not success:
        st.error("Could not read frame")
        break
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame,caption="Camera View",use_container_width=True)

# In this we create a single button in the center    
with st.columns([1,2,1])[1]:
    if st.button('Clear'):
        st.session_state.stop=False
        frame_placeholder.empty()
cam.release()