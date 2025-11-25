"""
Emotion Detector
----------------
Simple wrapper to handle the emotion prediction logic.
Uses the CNN model to guess emotions from face images.
"""

import numpy as np
import os
from core.ai_model import EmotionCNN, create_pretrained_model
from core.image_processor import ImagePreprocessor


class EmotionPredictor:
    def __init__(self, model_path='models/emotion_model.h5'):
        self.model_path = model_path
        self.preprocessor = ImagePreprocessor()
        
        # Standard 7 emotions for FER
        self.labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Color map for UI (RGB)
        # TODO: maybe add more vibrant colors later?
        self.colors = {
            'Angry': (255, 0, 0),      # Red
            'Disgust': (128, 0, 128),   # Purple
            'Fear': (139, 69, 19),      # Brown
            'Happy': (255, 215, 0),     # Gold
            'Sad': (0, 0, 255),         # Blue
            'Surprise': (255, 165, 0),  # Orange
            'Neutral': (128, 128, 128)  # Gray
        }
        
        self.model = None
        self._init_model()
    
    def _init_model(self):
        """Helper to load or create the model if it doesn't exist"""
        try:
            cnn = EmotionCNN()
            
            if os.path.exists(self.model_path):
                cnn.load_model(self.model_path)
                self.model = cnn.model
                print("Loaded pre-trained model!")
            else:
                print("No model found, creating a new one...")
                cnn.build_model()
                cnn.compile_model()
                self.model = cnn.model
                print("New model created (needs training!)")
                
        except Exception as e:
            print(f"Model init failed: {e}")
            # Fallback just in case
            cnn = create_pretrained_model()
            self.model = cnn.model
    
    def predict_emotion(self, face_img):
        """Predicts emotion for a single face crop"""
        try:
            # Prep image for the model
            processed = self.preprocessor.preprocess_face(face_img)
            
            # Get raw predictions
            raw_preds = self.model.predict(processed, verbose=0)
            probs = raw_preds[0]
            
            # Find the strongest emotion
            idx = np.argmax(probs)
            top_emotion = self.labels[idx]
            conf = probs[idx] * 100
            
            # Pack everything up
            all_emotions = {}
            for i, label in enumerate(self.labels):
                all_emotions[label] = float(probs[i] * 100)
            
            return {
                'dominant_emotion': top_emotion,  # keeping key names for compatibility
                'confidence': float(conf),
                'all_emotions': all_emotions,
                'emotion_color': self.colors[top_emotion]
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Return dummy data if something breaks
            return {
                'dominant_emotion': 'Unknown',
                'confidence': 0.0,
                'all_emotions': {l: 0.0 for l in self.labels},
                'emotion_color': (128, 128, 128)
            }
    
    def predict_from_image(self, image):
        """Main function to handle full images"""
        results = []
        
        try:
            # First, find all faces
            faces = self.preprocessor.detect_faces(image)
            
            if not faces:
                return []
            
            # Loop through each face found
            for i, (x, y, w, h) in enumerate(faces):
                # Cut out the face
                roi = self.preprocessor.extract_face_roi(image, (x, y, w, h))
                
                # Get the emotion
                res = self.predict_emotion(roi)
                
                # Add location data
                res['face_coords'] = (int(x), int(y), int(w), int(h))
                res['face_number'] = i + 1
                
                results.append(res)
            
            return results
            
        except Exception as e:
            print(f"Image processing failed: {e}")
            return []
    
    def annotate_image(self, image, preds):
        """Draws boxes and labels on the image"""
        # Work on a copy so we don't mess up the original
        out_img = np.array(image).copy()
        
        for p in preds:
            coords = p['face_coords']
            emotion = p['dominant_emotion']
            conf = p['confidence']
            color = p['emotion_color']
            
            # Draw the box
            out_img = self.preprocessor.draw_face_rectangle(
                out_img, coords, color=color, thickness=3
            )
            
            # Add the text
            out_img = self.preprocessor.add_emotion_label(
                out_img, coords, emotion, conf,
                text_color=color, bg_color=(0, 0, 0)
            )
        
        return out_img
    
    def get_emotion_statistics(self, preds):
        """Quick stats helper"""
        if not preds:
            return {
                'total_faces': 0,
                'dominant_emotions': {},
                'average_confidence': 0.0
            }
        
        total = len(preds)
        counts = {}
        total_conf = 0.0
        
        for p in preds:
            emo = p['dominant_emotion']
            counts[emo] = counts.get(emo, 0) + 1
            total_conf += p['confidence']
        
        return {
            'total_faces': total,
            'dominant_emotions': counts,
            'average_confidence': total_conf / total if total > 0 else 0.0
        }
