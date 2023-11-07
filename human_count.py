from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import imutils
import numpy as np

app = Flask(__name__)

# Function to perform human detection
def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    return frame

# Route to the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/detect', methods=['POST'])
def detect_people():
    if request.method == 'POST':
        # Get input type from the form
        input_type = request.form['input_type']

        # Perform human detection based on the input type
        if input_type == 'camera':
            # Open the camera and perform real-time detection
            # You may need to modify this part to display the results in real-time
            return "Camera mode is not supported in this example."

        elif input_type == 'image':
            # Process an image
            image_path = request.form['image_path']
            output_path = 'static/result.jpg'  # Set the path where the result image will be saved
            detectByPathImage(image_path, output_path)
            return redirect(url_for('result', filename='result.jpg'))

        elif input_type == 'video':
            # Process a video
            video_path = request.form['video_path']
            output_path = 'static/result.avi'  # Set the path where the result video will be saved
            detectByPathVideo(video_path, output_path)
            return redirect(url_for('result', filename='result.avi'))

    return "Invalid input type."

# Route to display the detection result
@app.route('/result/<filename>')
def result(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
