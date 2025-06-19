import os
import librosa
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import json
import matplotlib.pyplot as plt

# Set up Spotipy with your Spotify API credentials
SPOTIPY_CLIENT_ID = 'fb65558cefeb48a5a8fe0da6a931f9a1'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'  # Replace this with your actual client secret

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_CLIENT_SECRET))

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
    Analyzes a .wav file and extracts features including bpm, key, valence, and energy.

    Parameters:
    file_path (str): Path to the .wav file.

    Returns:
    dict: A dictionary containing the extracted features.
    """
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

    # Extract valence and energy using Spotipy
    track_id = get_spotify_track_id(file_path)
    if track_id:
        audio_features = sp.audio_features(track_id)[0]
        valence = audio_features['valence']
        energy = audio_features['energy']
    else:
        valence = None
        energy = None

    features = {
        'tempo': tempo,
        'chroma': chroma,
        'tonnetz': tonnetz,
        'valence': valence,
        'energy': energy
    }

    return features

def get_spotify_track_id(file_path):
    """
    Retrieves the Spotify track ID for a given audio file.

    Parameters:
    file_path (str): Path to the .wav file.

    Returns:
    str: The Spotify track ID, or None if not found.
    """
    # Implement your logic to retrieve the Spotify track ID based on the file path or metadata
    # For example, you can use the file name or metadata to search for the track on Spotify
    # and return the track ID if found.
    return None

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

# Load the analysis results from the JSON file
with open(r"C:\Users\Kenrm\repositories\music-prod\data\analysis_results.json", 'r') as f:
    analysis_results = json.load(f)

# Extract chroma features from the first analyzed file
chroma = np.array(analysis_results[0]['features']['chroma'])

# Plot the chroma features
plt.figure(figsize=(10, 4))
plt.imshow(chroma, aspect='auto', origin='lower', cmap='coolwarm')
plt.title('Chroma Features')
plt.xlabel('Time')
plt.ylabel('Pitch Class')
plt.colorbar()
plt.show()