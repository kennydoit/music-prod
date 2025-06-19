import os
import re

def remove_file_prefix(directory):
    """
    Renames .wav files in the specified directory by removing a 3-character prefix and dash.
    
    Parameters:
    directory (str): Path to the directory containing .wav files
    
    Example:
    ABC-song.wav -> song.wav
    XYZ-music.wav -> music.wav
    song.wav -> song.wav (unchanged)
    """
    # Pattern to match: 3 letters followed by a dash at start of filename
    pattern = r'^[A-Za-z]{3}-'
    
    for filename in os.listdir(directory):
        # Check if file is .wav and matches our pattern
        if filename.endswith('.wav') and re.match(pattern, filename):
            # Create the new filename by removing first 4 characters
            new_filename = filename[4:]
            
            # Get full file paths
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            try:
                # Rename the file
                os.rename(old_path, new_path)
                print(f'Renamed: {filename} -> {new_filename}')
            except OSError as e:
                print(f'Error renaming {filename}: {e}')

# Example usage
if __name__ == "__main__":
    # Replace with your directory path
    wav_directory = r"C:\Users\Kenrm\OneDrive\Documents\Image-Line\FL Studio\Projects\Stem Packages\BLZ-EDM Loops\Kick Loops"
    remove_file_prefix(wav_directory)