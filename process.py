import pandas as pd
from file import create_image_with_text, create_video_with_audio
import os
from time import sleep
import re

# Function to process the CSV and generate videos
def process_csv_and_create_videos(csv_file_path, audio_folder, output_folder="videos"):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    for _, row in df[335:].iterrows(): # df.iloc[400:].iterrows():
        chapter = row['chapter']
        verse = row['verse']
        sanskrit = row['sanskrit']
        translation = row['translation']
        
        sanskrit_cleaned = sanskrit[:-12]  # Remove extra characters
        shloka_number = f"{chapter}.{verse}"  # Use chapter and verse as shloka number

        if shloka_number:
            output_image_path = os.path.join(output_folder, f"{shloka_number}.png") 
            print(f"Creating image for Shloka {shloka_number} at {output_image_path}")
            create_image_with_text(output_image_path, sanskrit_cleaned, translation, shloka_number)
            
            audio_file_name = f"{chapter}-{verse}.MP3"
            audio_path = os.path.join(audio_folder, audio_file_name)
            
            output_video_path = os.path.join(output_folder, f"{shloka_number}.mp4")
            create_video_with_audio(output_image_path, audio_path, output_video_path)
            # sleep(1)



csv_file_path = "/home/divyansh/Desktop/bhagwadGeeta/ProjectsSection/Bhagwad_Gita/Bhagwad_Gita_Verses_English_Questions.csv"  # Path to the CSV file
audio_folder = "/home/divyansh/Desktop/bhagwadGeeta/ProjectsSection/Bhagwad_Gita/Chant_Audio"  # Path to the folder with audio files

# Process CSV and create videos
process_csv_and_create_videos(csv_file_path, audio_folder)
