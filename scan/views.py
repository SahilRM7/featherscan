from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import json
import librosa
import numpy as np
import tensorflow as tf

# Example: dummy prediction function (replace with real ML logic)
def predict_bird_species(image_path):
    # For demonstration purposes
    return "Indian Peafowl", 0.97  # Example prediction and confidence

def image_scan(request):
    return render(request, 'imgscan.html')

def predict_image(request):
    if request.method == 'POST' and request.FILES['bird_image']:
        image = request.FILES['bird_image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)

        # Run your ML model here
        predicted_species, confidence = predict_bird_species(fs.path(filename))

        context = {
            'file_url': file_url,
            'predicted_species': predicted_species,
            'confidence': round(confidence * 100, 2)
        }
        return render(request, 'imgscan_result.html', context)

    return render(request, 'imgscan.html')

# views.py




def audio_scan(request):
    result = None

    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']

        # Save uploaded file to media directory
        fs = FileSystemStorage()
        filename = fs.save(audio_file.name, audio_file)
        file_path = fs.path(filename)

        try:
            # Load label dictionary
            with open(os.path.join(settings.BASE_DIR, 'prediction.json'), 'r') as f:
                prediction_dict = json.load(f)

            # Load audio and extract MFCC
            audio, sample_rate = librosa.load(file_path)
            mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            mfccs_features = np.mean(mfccs_features, axis=1)
            mfccs_features = np.expand_dims(mfccs_features, axis=0)
            mfccs_features = np.expand_dims(mfccs_features, axis=2)

            # Convert to tensor and predict
            mfccs_tensors = tf.convert_to_tensor(mfccs_features, dtype=tf.float32)
            model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, 'model.h5'))
            prediction = model.predict(mfccs_tensors)

            target_label = np.argmax(prediction)
            predicted_class = prediction_dict[str(target_label)]
            confidence = round(np.max(prediction) * 100, 2)

            result = f"{predicted_class} ({confidence}% match)"

        except Exception as e:
            result = f"Error processing audio: {e}"

        # Remove the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

    return render(request, 'audioscan.html', {'result': result})
