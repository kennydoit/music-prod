import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the analysis results from the JSON file
with open(r"C:\Users\Kenrm\repositories\music-prod\data\analysis_results.json", 'r') as f:
    analysis_results = json.load(f)

file_names = [result['file'] for result in analysis_results]
tempos = [result['features']['tempo'] for result in analysis_results if result['features']['tempo'] is not None]
average_tempo = np.mean(tempos)
print(f"Average Tempo: {average_tempo:.2f} BPM")

rms_values = [np.mean(result['features']['rms']) for result in analysis_results if np.mean(result['features']['rms']) is not None]
average_rms = np.mean(rms_values)
print(f"Average RMS Energy: {average_rms:.2f}")

spectral_bandwidths = [np.mean(result['features']['spectral_bandwidth']) for result in analysis_results if np.mean(result['features']['spectral_bandwidth']) is not None]
average_spectral_bandwidth = np.mean(spectral_bandwidths)
print(f"Average Spectral Bandwidth: {average_spectral_bandwidth:.2f} Hz")

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

# Extract spectral centroid from the first analyzed file
spectral_centroid = np.array(analysis_results[0]['features']['spectral_centroid'])

# Plot the spectral centroid
plt.figure(figsize=(10, 4))
plt.plot(spectral_centroid[0])
plt.title('Spectral Centroid')
plt.xlabel('Time')
plt.ylabel('Frequency (Hz)')
plt.show()

# Extract spectral bandwidth from the first analyzed file
spectral_bandwidth = np.array(analysis_results[0]['features']['spectral_bandwidth'])

# Plot the spectral bandwidth
plt.figure(figsize=(10, 4))
plt.plot(spectral_bandwidth[0])
plt.title('Spectral Bandwidth')
plt.xlabel('Time')
plt.ylabel('Bandwidth (Hz)')
plt.show()

# Extract spectral contrast from the first analyzed file
spectral_contrast = np.array(analysis_results[0]['features']['spectral_contrast'])

# Plot the spectral contrast
plt.figure(figsize=(10, 4))
plt.imshow(spectral_contrast, aspect='auto', origin='lower', cmap='coolwarm')
plt.title('Spectral Contrast')
plt.xlabel('Time')
plt.ylabel('Frequency Bands')
plt.colorbar()
plt.show()

# Extract spectral flatness from the first analyzed file
spectral_flatness = np.array(analysis_results[0]['features']['spectral_flatness'])

# Plot the spectral flatness
plt.figure(figsize=(10, 4))
plt.plot(spectral_flatness[0])
plt.title('Spectral Flatness')
plt.xlabel('Time')
plt.ylabel('Flatness')
plt.show()

# Extract spectral rolloff from the first analyzed file
spectral_rolloff = np.array(analysis_results[0]['features']['spectral_rolloff'])

# Plot the spectral rolloff
plt.figure(figsize=(10, 4))
plt.plot(spectral_rolloff[0])
plt.title('Spectral Rolloff')
plt.xlabel('Time')
plt.ylabel('Frequency (Hz)')
plt.show()

# Filter out None values from file_names, tempos, and rms_values
filtered_file_names = [result['file'] for result in analysis_results if result['features']['tempo'] is not None]
filtered_rms_values = [np.mean(result['features']['rms']) for result in analysis_results if np.mean(result['features']['rms']) is not None]

plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.bar(filtered_file_names, tempos)
plt.title('Tempo of Each File')
plt.xlabel('File')
plt.ylabel('Tempo (BPM)')
plt.xticks(rotation=90)

plt.subplot(2, 1, 2)
plt.bar(filtered_file_names, filtered_rms_values)
plt.title('RMS Energy of Each File')
plt.xlabel('File')
plt.ylabel('RMS Energy')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()

# Create a DataFrame from the analysis results
data = {
    'tempo': [result['features']['tempo'] for result in analysis_results if result['features']['tempo'] is not None],
    'rms': [np.mean(result['features']['rms']) for result in analysis_results if np.mean(result['features']['rms']) is not None],
    'spectral_centroid': [np.mean(result['features']['spectral_centroid']) for result in analysis_results if np.mean(result['features']['spectral_centroid']) is not None],
    'spectral_bandwidth': [np.mean(result['features']['spectral_bandwidth']) for result in analysis_results if np.mean(result['features']['spectral_bandwidth']) is not None]
}

df = pd.DataFrame(data)

# Calculate the correlation matrix
correlation_matrix = df.corr()
print(correlation_matrix)