import os

def rename_wav_files(directory, substring, replacement):
    """
    Renames .wav files in the specified directory by replacing a substring in the file names.

    Parameters:
    directory (str): Path to the directory containing .wav files.
    substring (str): The substring to search for in the file names.
    replacement (str): The string to replace the substring with.

    Returns:
    None
    """
    for file_name in os.listdir(directory):
        # Check if the file is a .wav file and contains the substring
        if file_name.endswith('.wav') and substring in file_name:
            original_path = os.path.join(directory, file_name)
            new_file_name = file_name.replace(substring, replacement)
            new_path = os.path.join(directory, new_file_name)

            # Rename the file
            os.rename(original_path, new_path)
            print(f'Renamed: {original_path} to {new_path}')

# Example usage
# rename_wav_files(
#     r"C:\Users\Kenrm\OneDrive\Documents\Image-Line\FL Studio\Projects\01_Melodic Stems\Melodic Stems",
#     'Pulsar Star', 'AKO-Pulsar'
#     )


# rename_wav_files(
#     r"C:\Users\Kenrm\OneDrive\Documents\Image-Line\FL Studio\Projects\01_Bass Stems\Bass Stems",
#     'Crawl', 'AUX-Crawl'
#     )

# rename_wav_files(
#     r"C:\Users\Kenrm\OneDrive\Documents\Image-Line\FL Studio\Projects\02_Drum Stems\Drum Stems\Kick Stems",
#     'Triple Thump', 'AYB-Triple Thump'
#     )

rename_wav_files(
    r"C:\Users\Kenrm\OneDrive\Documents\Image-Line\FL Studio\Projects\02_Drum Stems\Drum Stems\Kick Stems",
    '130 BPM', 'AsIs_130 BPM'
    )