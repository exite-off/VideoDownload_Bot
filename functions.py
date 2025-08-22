import ytmusicapi
import yt_dlp

# configure yt_dlp
base_url = 'https://music.youtube.com/watch?v='
yt = ytmusicapi.YTMusic()
cookie_file_path = 'cookies.txt'

# Download audio from YouTube music
async def download_audio(yt_url, query = 'result') -> None:
    ydl_opts = {
        'cookies': cookie_file_path,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': f'{query}.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
