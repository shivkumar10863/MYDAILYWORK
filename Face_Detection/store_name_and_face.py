import streamlit as st
import cv2
import os

st.title("Store Face with Name")
# Session variables these are define at once time at the start 
if "stop" not in st.session_state:
    st.session_state.stop = True

if "picture" not in st.session_state:
    st.session_state.picture = None

# Create folder if it doesn't exist
folder = "Face_Detection\\known_faces"
if not os.path.exists(folder):
    os.makedirs(folder)

# Enter name of the people
name = st.text_input("Enter Name")

# Open the webcam
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    st.error("Could not open webcam")
    st.stop()
# Create a placeholder for the video feed
frame_placeholder = st.empty()
col1,col2,col3 = st.columns(3)
with col1:
    if st.button("Start Camera"):
        st.session_state.stop = False
with col2:
    if st.button("Stop Camera"):
        st.session_state.stop = True
        cam.release()
with col3:
    if st.button("Take picture"):
            if st.session_state.picture is not None and name:
                print("Picture taken")
                # Save image
                path = os.path.join(folder,f"{name}.jpg")
                cv2.imwrite(path,st.session_state.picture)
                st.success(f"{name} face saved successfully")
                frame_placeholder.image(st.session_state.picture,caption=f"Saved as {name}.jpg")
                st.session_state.stop = True
# Read frames from the webcam and perform face detection
while st.session_state.stop is False:
    success,st.session_state.picture = cam.read()
    if not success:
        st.error("Could not read frame")
        st.stop()
    # Convert BGR → RGB
    display = cv2.cvtColor(st.session_state.picture,cv2.COLOR_BGR2RGB)
    frame_placeholder.image(display,caption=f"Camera view",use_container_width=True)