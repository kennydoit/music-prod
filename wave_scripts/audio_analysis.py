from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt

# Load audio file
[Fs, x] = audioBasicIO.read_audio_file(r'G:\02_FL Data\Patches\Packs\Synths\Loops\Cymatics - Odyssey EDM Sample Pack\Cymatics - Odyssey Breakdown Loop 1 - 90 BPM E Min Arp.wav')

# Feature extraction
features, feature_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs)

# Plot features
plt.subplot(2,1,1); plt.plot(features[0,:]); plt.xlabel('Frame no'); plt.ylabel(feature_names[0])
plt.subplot(2,1,2); plt.plot(features[1,:]); plt.xlabel('Frame no'); plt.ylabel(feature_names[1])
plt.tight_layout()
plt.show()