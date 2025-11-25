"""
Model Training Script (Template)
This script provides a template for training the emotion recognition model

Note: You'll need a labeled dataset (e.g., FER2013) to train the model
"""

import numpy as np
from logic.model import EmotionCNN
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os


def train_emotion_model(train_data_path, val_data_path, epochs=50, batch_size=32):
    """
    Train the emotion recognition model
    
    Args:
        train_data_path: Path to training data directory
        val_data_path: Path to validation data directory
        epochs: Number of training epochs
        batch_size: Batch size for training
    """
    
    # Initialize model
    print("🔧 Initializing model...")
    emotion_model = EmotionCNN()
    emotion_model.build_model()
    emotion_model.compile_model(learning_rate=0.001)
    
    # Print model summary
    print("\n📊 Model Architecture:")
    emotion_model.get_model_summary()
    
    # Data augmentation for training
    print("\n🔄 Setting up data augmentation...")
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        shear_range=0.2,
        fill_mode='nearest'
    )
    
    # Validation data (no augmentation)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Note: This assumes your data is organized in folders by emotion class
    # Example structure:
    # train_data_path/
    #   ├── angry/
    #   ├── disgust/
    #   ├── fear/
    #   ├── happy/
    #   ├── sad/
    #   ├── surprise/
    #   └── neutral/
    
    try:
        # Load training data
        train_generator = train_datagen.flow_from_directory(
            train_data_path,
            target_size=(48, 48),
            color_mode='grayscale',
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=True
        )
        
        # Load validation data
        val_generator = val_datagen.flow_from_directory(
            val_data_path,
            target_size=(48, 48),
            color_mode='grayscale',
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"\n✓ Found {train_generator.samples} training images")
        print(f"✓ Found {val_generator.samples} validation images")
        print(f"✓ Classes: {list(train_generator.class_indices.keys())}")
        
    except Exception as e:
        print(f"\n⚠ Error loading data: {e}")
        print("\n💡 To train the model, you need to:")
        print("   1. Download a facial emotion dataset (e.g., FER2013)")
        print("   2. Organize images into folders by emotion class")
        print("   3. Update train_data_path and val_data_path")
        return
    
    # Setup callbacks
    print("\n⚙️ Setting up training callbacks...")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            'models/emotion_model_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping to prevent overfitting
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate when validation loss plateaus
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train the model
    print(f"\n🚀 Starting training for {epochs} epochs...")
    
    history = emotion_model.model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=val_generator.samples // batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    print("\n💾 Saving final model...")
    emotion_model.save_model('models/emotion_model.h5')
    
    # Print training results
    print("\n✅ Training completed!")
    print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    
    return history


def create_sample_training_structure():
    """
    Create sample directory structure for training data
    """
    print("\n📁 Creating sample training directory structure...")
    
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    for split in ['train', 'validation']:
        for emotion in emotions:
            path = f'data/{split}/{emotion}'
            os.makedirs(path, exist_ok=True)
    
    print("✓ Directory structure created at 'data/'")
    print("\n💡 Next steps:")
    print("   1. Download FER2013 or another emotion dataset")
    print("   2. Place images in the corresponding emotion folders")
    print("   3. Run this training script")


if __name__ == "__main__":
    print("🎭 Emotion Recognition Model Training")
    print("=" * 50)
    
    # Check if training data exists
    if not os.path.exists('data/train') or not os.path.exists('data/validation'):
        print("\n⚠ Training data not found!")
        create_sample_training_structure()
        print("\n" + "=" * 50)
        print("📚 TRAINING INSTRUCTIONS:")
        print("=" * 50)
        print("""
To train the emotion recognition model:

1. Download a dataset:
   - FER2013: https://www.kaggle.com/datasets/msambare/fer2013
   - CK+: http://www.consortium.ri.cmu.edu/ckagree/
   - JAFFE: https://zenodo.org/record/3451524

2. Organize your data in the created structure:
   data/
   ├── train/
   │   ├── angry/
   │   ├── disgust/
   │   ├── fear/
   │   ├── happy/
   │   ├── sad/
   │   ├── surprise/
   │   └── neutral/
   └── validation/
       ├── angry/
       ├── disgust/
       ├── fear/
       ├── happy/
       ├── sad/
       ├── surprise/
       └── neutral/

3. Run the training script:
   python logic/train.py

4. The trained model will be saved to 'models/emotion_model.h5'
        """)
    else:
        # Training data exists, start training
        train_emotion_model(
            train_data_path='data/train',
            val_data_path='data/validation',
            epochs=50,
            batch_size=32
        )
