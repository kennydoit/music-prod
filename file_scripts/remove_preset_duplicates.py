import os

def remove_duplicates(new_presets_folder, to_dedup_folder):
    """
    Removes duplicate files from the 'To Dedup' folder if they also exist in the 'New Presets' folder.

    Parameters:
    new_presets_folder (str): Path to the 'New Presets' folder.
    to_dedup_folder (str): Path to the 'To Dedup' folder.

    Returns:
    None
    """
    # Get the list of files in the 'New Presets' folder
    new_presets_files = set(os.listdir(new_presets_folder))

    # Get the list of files in the 'To Dedup' folder
    to_dedup_files = os.listdir(to_dedup_folder)

    # Iterate over the files in the 'To Dedup' folder
    for file_name in to_dedup_files:
        # Check if the file also exists in the 'New Presets' folder
        if file_name in new_presets_files:
            # Construct the full file path
            file_path = os.path.join(to_dedup_folder, file_name)
            # Remove the duplicate file
            os.remove(file_path)
            print(f"Removed duplicate file: {file_path}")

# Example usage
new_presets_folder = r"C:\Users\Kenrm\repositories\music-prod\New Presets"
to_dedup_folder = r"C:\Users\Kenrm\repositories\music-prod\To Dedup"
remove_duplicates(new_presets_folder, to_dedup_folder)