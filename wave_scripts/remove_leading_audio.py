# -*- coding: utf-8 -*-


from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import logging
import os

logging.basicConfig(level=logging.INFO)

def remove_leading_silence(input_file, output_file, silence_thresh=-50, min_silence_len=1000):
    """
    Removes leading silence from an audio file.

    Parameters:
    input_file (str): Path to the input audio file.
    output_file (str): Path to save the output audio file.
    silence_thresh (int): Silence threshold in dB. Default is -50 dB.
    min_silence_len (int): Minimum length of silence in milliseconds. Default is 1000 ms.

    Returns:
    None
    """
    audio = AudioSegment.from_wav(input_file)

    # Detect non-silent parts (returns a list of tuples representing non-silent ranges)
    non_silent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    if non_silent_ranges:
        # Get the start of the first non-silent range
        start_trim = non_silent_ranges[0][0]

        if start_trim < min_silence_len:
            logging.info(f"The leading audio is shorter than the minimum threshold of {min_silence_len}ms. No output file created.")
            return None
        
        # Trim the silence from the start
        trimmed_audio = audio[start_trim:]
        if trimmed_audio:
            trimmed_audio.export(output_file, format="wav")
        logging.info("!!! Silent parts found in the audio. Output file created !!!")
    else:
        logging.info("No non-silent parts found in the audio. No output file created.")
        return None

def process_folder(folder_path, silence_thresh=-50, min_silence_len=250):
    """
    Processes all .wav files in a given folder and its sub-folders to remove leading silence.

    Parameters:
    folder_path (str): Path to the folder containing .wav files.
    silence_thresh (int): Silence threshold in dB. Default is -50 dB.
    min_silence_len (int): Minimum length of silence in milliseconds. Default is 250 ms.

    Returns:
    None
    """
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".wav"):
                input_file = os.path.join(root, filename)
                logging.info(f"Processing file: {input_file}")
                remove_leading_silence(input_file, input_file, silence_thresh, min_silence_len)

# Example usage
folder_path = "C://Program Files//Image-Line//Packs//Vocals//Black Octopus Sound - Katty Heath Vocal Sample Pack"
process_folder(folder_path, -50, 150)


