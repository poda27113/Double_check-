import os
import hashlib
import zipfile

def hash_file(file_path):
    """Generate a hash for the file using SHA-256"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def remove_duplicate_files(directory):
    """Check for duplicate files by content and remove duplicates"""
    seen_files = {}
    deleted_files = []
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = hash_file(file_path)
            
            if file_hash in seen_files:
                # Duplicate found, remove it
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"Deleted duplicate: {file_path}")
            else:
                seen_files[file_hash] = file_path

    return deleted_files

def zip_folder(folder_path, output_zip):
    """Zip the folder after duplicates are removed"""
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print(f"Folder zipped successfully as: {output_zip}")

# Example usage for Windows
folder_to_check = r'C:\Users\USER\Music'  # Path to your Music folder
output_zip = r'C:\Users\USER\Documents\music_folder_zipped.zip'  # Path where you want the zip file

# Step 1: Remove duplicates
removed_files = remove_duplicate_files(folder_to_check)

# Step 2: Zip the folder
zip_folder(folder_to_check, output_zip)