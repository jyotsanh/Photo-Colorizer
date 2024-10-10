import os
import yt_dlp

def download_playlist_as_mp3(playlist_url, output_path=None):
    # If no output path is provided, set the default to a 'yt_music' folder on the desktop
    if output_path is None or output_path.strip() == "":
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = os.path.join(desktop_path, "yt_music")
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print("Playlist download complete!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Main execution
if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_folder = input("Enter the output folder path (or press Enter to save on Desktop in 'yt_music'): ")

    download_playlist_as_mp3(playlist_url, output_folder)
