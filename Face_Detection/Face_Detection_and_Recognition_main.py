import streamlit as st
import cv2
import face_recognition
import os
        
st.title("Live Face Detection & Recognition")
# Session variables these are define at once time at the start 
if "stop" not in st.session_state:
    st.session_state.stop = True
# Load the chosen haar cascade model
face_cascade = cv2.CascadeClassifier("Face_Detection/haarcascade_frontalface_default.xml")
# Store known face data
known_encodings = []
known_names = []

folder = "Face_Detection\\known_faces"

# Load known faces
for file in os.listdir(folder):
    path = os.path.join(folder, file)
    image = face_recognition.load_image_file(path)
    encodings = face_recognition.face_encodings(image)

    # Skip image if no face found
    if len(encodings) > 0:
        known_encodings.append(encodings[0])
        known_names.append(file.split(".")[0])

# Open the webcam
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

if not cam.isOpened():
    st.error("Could not open webcam")
    st.stop()
# Create a placeholder for the video feed
frame_placeholder = st.empty()
col1,col2 = st.columns(2)
with col1:
    if st.button("Start Camera"):
        st.session_state.stop=False
with col2:
    if st.button("Stop Camera"):
        st.session_state.stop=True
        cam.release()
# Read frames from the webcam and perform face detection
while st.session_state.stop is False:
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
    # Recognition
    locations = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame,locations)

    for (top, right, bottom, left), encoding in zip(locations,encodings):
        name = "Unknown"
        matches = face_recognition.compare_faces(known_encodings,encoding)
        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
        cv2.putText(frame,name,(left, top-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
    frame_placeholder.image(frame,caption=f"Detected Faces: {len(faces)}",use_container_width=True)
    cv2.waitKey(21)
cam.release()