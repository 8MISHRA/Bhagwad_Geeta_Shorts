###################################################################################
# final code

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, concatenate_videoclips

# Function to wrap text for English
def wrap_text(text, font, width, draw):
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        if text_width <= width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# Corrected function to split long Hindi text
def split_long_text(text):
    def split_by_midpoint(part):
        if len(part) <= 25:
            return [part]
        mid = len(part) // 2
        left_space = part.rfind(' ', 0, mid)
        right_space = part.find(' ', mid)
        if left_space != -1 and (mid - left_space <= right_space - mid or right_space == -1):
            return [part[:left_space].strip(), part[left_space + 1:].strip()]
        elif right_space != -1:
            return [part[:right_space].strip(), part[right_space + 1:].strip()]
        else:
            return [part]

    parts = text.split('|')
    final_parts = []

    for i, part in enumerate(parts):
        split_lines = split_by_midpoint(part.strip())
        final_parts.extend(split_lines)
        if i < len(parts) - 1:
            final_parts[-1] += ' |'  # Re-append '|' to the last line of this part

    # Add " ||" only to the last line
    final_parts[-1] = final_parts[-1].rstrip(' |') + " ||"
    return final_parts


def create_image_with_text(output_image_path, sanskrit, translation, shloka_number):
    width, height = 486, 864
    # dark_blue = (30, 58, 140)
    dark_blue = (27, 51, 128)
    image = Image.new("RGB", (width, height), dark_blue)
    draw = ImageDraw.Draw(image)

    font_path = "Nirmala.ttf"  # You can keep the other fonts as they are
    title_font_path1 = "Serif.ttf"  # Use serif font for the title
    title_font_path = "Arial.ttf"
    hindi_font = ImageFont.truetype(font_path, 35)
    english_font = ImageFont.truetype(title_font_path1, 35)
    title_font = ImageFont.truetype(title_font_path, 40)
    
    title_text = f"Bhagavad Gita {shloka_number}"  # Updated title
    title_color = "white"

    # Title
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    title_x, title_y = (width - title_width) // 2, 35
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.text((title_x + dx, title_y + dy), title_text, fill=title_color, font=title_font)
    draw.text((title_x, title_y), title_text, fill=title_color, font=title_font)

    y_text = title_y + title_height + 80
    shloka_text = sanskrit
    # top_text_color = (255, 215, 0)  # Updated color
    top_text_color = (253, 210, 0)

    parts = split_long_text(shloka_text)
    for part in parts:
        text_bbox = draw.textbbox((0, 0), part, font=hindi_font)
        text_width = text_bbox[2] - text_bbox[0]
        x_position = (width - text_width) // 2
        draw.text((x_position, y_text), part, fill=top_text_color, font=hindi_font)
        y_text += 55

    bottom_text = translation
    bottom_text_color = (255, 215, 0) 
    lines = wrap_text(bottom_text, english_font, width-75, draw)
    y_text = height - 450 
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=english_font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        draw.text(((width - text_width) // 2, y_text), line, fill=bottom_text_color, font=english_font)
        y_text += text_height + 10

    image.save(output_image_path)
    print(f"Image saved to {output_image_path}")





# def create_video_with_audio(image_path, audio_path, output_video_path):
#     image_clip = ImageClip(image_path).set_duration(9.5)
#     audio_clip = AudioFileClip(audio_path)
#     blue_bg_clip = ColorClip(size=(486, 864), color=(30, 58, 150)).set_duration(1)
#     image_clip = image_clip.set_opacity(0).fadein(2)
#     video_clip = concatenate_videoclips([blue_bg_clip, image_clip.set_audio(audio_clip)])
#     video_clip.write_videofile(output_video_path, codec="libx264", fps=24)
#     print(f"Video saved to {output_video_path}")


from moviepy.editor import ImageClip, AudioFileClip, ColorClip, concatenate_videoclips, concatenate_audioclips
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os

def create_video_with_audio(image_path, audio_path, output_video_path):
    image_clip = ImageClip(image_path).set_duration(9.5)

    # Load the actual audio clip
    audio_clip = AudioFileClip(audio_path)

    # Create a silent audio clip (1 second of silence at 44100 Hz sample rate)
    silent_audio = np.zeros((44100,))  # 1 second of silence at 44100 Hz
    silent_audio_tempfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    silent_audio_path = silent_audio_tempfile.name
    
    # Save the silent audio to a temporary file
    write(silent_audio_path, 44100, silent_audio)

    # Load the silent audio file using AudioFileClip
    silent_audio_clip = AudioFileClip(silent_audio_path)

    # Concatenate the silent audio with the actual audio
    audio_clip = concatenate_audioclips([silent_audio_clip, audio_clip])

    # Create a blue background clip for 1 second
    blue_bg_clip = ColorClip(size=(486, 864), color=(30, 58, 150)).set_duration(1)

    # Make the image fade in over 2 seconds and set opacity
    image_clip = image_clip.set_opacity(0).fadein(2)

    # Combine the clips (blue background first, then image with delayed audio)
    video_clip = concatenate_videoclips([blue_bg_clip, image_clip.set_audio(audio_clip)])

    # Write the video to file with a codec and fps setting
    video_clip.write_videofile(output_video_path, codec="libx264", fps=24)
    print(f"Video saved to {output_video_path}")

    # Clean up the temporary silent audio file
    os.remove(silent_audio_path)
