"""
CNN Model Architecture
----------------------
This is where the magic happens!
A custom CNN built with Keras to detect emotions.
"""

import tensorflow as tf
from tensorflow import keras
from keras import layers, models
import os


class EmotionCNN:
    def __init__(self, input_shape=(48, 48, 1), num_classes=7):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        
    def build_model(self):
        """
        Constructs the CNN.
        I used 4 conv blocks to make sure we catch all the details (eyes, mouth, etc).
        """
        model = models.Sequential([
            # Block 1: Basic edges and shapes
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25), # Prevent overfitting!
            
            # Block 2: More complex features (eyes/eyebrows)
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3: Mouth and expressions
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 4: High-level facial patterns
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Classifier
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output: 7 emotions
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        self.model = model
        return model
    
    def compile_model(self, lr=0.001):
        """Sets up the optimizer and loss function"""
        if self.model is None:
            self.build_model()
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=lr),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
    def save_model(self, filepath='models/emotion_model.h5'):
        """Saves weights to disk"""
        if self.model:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            self.model.save(filepath)
            print(f"Saved model to {filepath}")
    
    def load_model(self, filepath='models/emotion_model.h5'):
        """Loads weights from disk"""
        if os.path.exists(filepath):
            self.model = keras.models.load_model(filepath)
            print(f"Loaded model from {filepath}")
            return True
        else:
            print(f"Could not find model at {filepath}")
            return False


def create_pretrained_model():
    """Quick helper to get a fresh model"""
    cnn = EmotionCNN()
    cnn.build_model()
    cnn.compile_model()
    return cnn
