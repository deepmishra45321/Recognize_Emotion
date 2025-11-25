"""
Image Preprocessor
------------------
Helper class to handle all the OpenCV stuff.
Detects faces, crops them, and makes them ready for the model.
"""

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:
    def __init__(self):
        # Using Haar Cascades because they are fast and reliable enough
        # TODO: maybe switch to MTCNN later if accuracy is an issue?
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Eye detector (just for fun/extra features)
        eye_path = cv2.data.haarcascades + 'haarcascade_eye.xml'
        self.eye_cascade = cv2.CascadeClassifier(eye_path)
        
    def detect_faces(self, image, scale_factor=1.1, min_neighbors=5):
        """Finds faces in the image"""
        # OpenCV needs numpy arrays, not PIL images
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Grayscale is faster and easier for detection
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # The actual detection magic
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=scale_factor, 
            minNeighbors=min_neighbors,
            minSize=(30, 30)
        )
        
        return faces
    
    def preprocess_face(self, face_img, target_size=(48, 48)):
        """Prepares a face crop for the CNN"""
        # Make sure it's grayscale
        if len(face_img.shape) == 3:
            gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)
        else:
            gray = face_img
        
        # Resize to what the model expects (48x48)
        resized = cv2.resize(gray, target_size)
        
        # Normalize to 0-1 range (neural nets love small numbers)
        normalized = resized / 255.0
        
        # Add the weird dimensions Keras needs (batch_size, height, width, channels)
        processed = normalized.reshape(1, target_size[0], target_size[1], 1)
        
        return processed
    
    def extract_face_roi(self, image, coords):
        """Cuts out the face from the full image"""
        x, y, w, h = coords
        
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Slicing the array to get the face
        roi = image[y:y+h, x:x+w]
        return roi
    
    def draw_face_rectangle(self, image, coords, color=(0, 255, 0), thickness=2):
        """Draws a box around the face"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        out_img = image.copy()
        x, y, w, h = coords
        cv2.rectangle(out_img, (x, y), (x+w, y+h), color, thickness)
        
        return out_img
    
    def add_emotion_label(self, image, coords, text, conf, 
                         text_color=(0, 255, 0), bg_color=(0, 0, 0)):
        """Adds the emotion text above the face"""
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        out_img = image.copy()
        x, y, w, h = coords
        
        label = f"{text}: {conf:.1f}%"
        
        # Figure out where to put the text
        text_x = x
        text_y = y - 10 if y > 30 else y + h + 20
        
        # Text settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.6
        thick = 2
        
        # Draw a nice background box for readability
        (t_w, t_h), _ = cv2.getTextSize(label, font, scale, thick)
        cv2.rectangle(out_img, 
                     (text_x, text_y - t_h - 5),
                     (text_x + t_w, text_y + 5),
                     bg_color, -1)
        
        # Draw the actual text
        cv2.putText(out_img, label, (text_x, text_y), font, scale, text_color, thick)
        
        return out_img
