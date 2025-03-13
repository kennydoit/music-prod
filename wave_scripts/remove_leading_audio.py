# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import logging

logging.basicConfig(level=logging.INFO)

def remove_leading_silence(input_file, output_file, silence_thresh=-50, min_silence_len=1000):
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

#%%

remove_leading_silence("D://Audio//KCJ_Am_128_Vocal_Phrase_Loop_GiveMeSomething_Wet.wav", 
                       "D://Audio//KCJ_Am_128_Vocal_Phrase_Loop_GiveMeSomething_Wet.wav",
                       -40, 
                       250)


#%%

import os
import logging

logging.basicConfig(level=logging.INFO)

def process_folder(folder_path, silence_thresh=-50, min_silence_len=250):
    for filename in os.listdir(folder_path):
        if filename.endswith(".wav"):
            input_file = os.path.join(folder_path, filename)
            remove_leading_silence(input_file, input_file, silence_thresh, min_silence_len)

# Example usage
folder_path = "C://Program Files//Image-Line//Packs//Vocals//Black Octopus Sound - Katty Heath Vocal Sample Pack"


process_folder(folder_path, -50, 150)


