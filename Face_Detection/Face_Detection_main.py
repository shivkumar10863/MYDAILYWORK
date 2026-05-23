import streamlit as st
import cv2

st.title("Live Face Detection")
stop=True
# Select the model of haar cascade
cascade_option = st.selectbox(
    "Choose Model",
    [
        "Face_Detection\haarcascade_frontalcatface_extended.xml",
        "Face_Detection\haarcascade_frontalface_alt.xml",
        "Face_Detection\haarcascade_frontalface_alt2.xml",
        "Face_Detection\haarcascade_frontalface_default.xml"
    ]
)

# Load the chosen haar cascade model
face_cascade = cv2.CascadeClassifier(cascade_option)

# Open the webcam
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    st.error("Could not open webcam")
    st.stop()
# Create a placeholder for the video feed
frame_placeholder = st.empty()
if st.button("Start Camera"):
    stop = False
if st.button("Stop Camera"):
    stop = True
# Read frames from the webcam and perform face detection
while not stop:
    success, frame = cam.read()
    if not success:
        st.error("Could not read frame")
        break
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30)
    )

    # Draw rectangles on the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0),2)

    # Convert BGR → RGB
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    frame_placeholder.image(frame,caption=f"Detected Faces: {len(faces)}",use_container_width=True)
cam.release()