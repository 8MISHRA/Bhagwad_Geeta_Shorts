import os

def rename_files(folder_path, prefix):
    try:
        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print("The specified folder does not exist.")
            return
        
        # List all files in the folder
        files = os.listdir(folder_path)
        
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            # Ensure we're working only on files, not directories
            if os.path.isfile(file_path):
                new_name = f"{prefix}{file_name}"
                new_file_path = os.path.join(folder_path, new_name)
                
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_name} -> {new_name}")
        
        print("All files have been renamed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
folder_path = "/home/divyansh/Desktop/BhagwadGeetaShorts/Bhagwad_Geeta_Shorts/9"
rename_files(folder_path, "Bhagavad Gita ")

