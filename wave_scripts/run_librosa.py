import os
import librosa
import numpy as np
import json

# Custom JSON encoder to handle NumPy arrays
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.float32) or isinstance(obj, np.float64):
            return float(obj)
        if isinstance(obj, np.int64) or isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

def analyze_audio(file_path):
    """
    Analyzes a .wav file and extracts features including bpm, key, and additional audio features.

    Parameters:
    file_path (str): Path to the .wav file.

    Returns:
    dict: A dictionary containing the extracted features.
    """
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    spectral_flatness = librosa.feature.spectral_flatness(y=y)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

    features = {
        'tempo': tempo,
        'chroma': chroma,
        'tonnetz': tonnetz,
        'rms': rms,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'spectral_contrast': spectral_contrast,
        'spectral_flatness': spectral_flatness,
        'spectral_rolloff': spectral_rolloff
    }

    return features

def analyze_folder(folder_path, output_file):
    """
    Analyzes all .wav files in a given folder and extracts features.

    Parameters:
    folder_path (str): Path to the folder containing .wav files.
    output_file (str): Path to the output JSON file.

    Returns:
    None
    """
    results = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".wav"):
                file_path = os.path.join(root, filename)
                print(f"Analyzing file: {file_path}")
                try:
                    features = analyze_audio(file_path)
                    results.append({
                        'file': file_path,
                        'features': features
                    })
                except Exception as e:
                    print(f"Error analyzing {filename}: {str(e)}")

    # Write the results to the output file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4, cls=NumpyEncoder)

# Example usage
folder_path = r"C:\Users\Kenrm\repositories\music-prod\data\Wave Files"
output_file = r"C:\Users\Kenrm\repositories\music-prod\data\analysis_results.json"
analyze_folder(folder_path, output_file)