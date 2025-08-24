from aiogram.types import (Message, FSInputFile)
from aiogram import F, Router
from config import whitelist
from ytmusicapi.exceptions import YTMusicUserError
import hashlib
import functions
import os
from pydub import AudioSegment

router = Router()

# voice converter function
async def voice_send(message: Message) -> None:
    # get info about file
    audio = message.audio
    duration: int = audio.duration
    file_id: str = audio.file_id
    # download file and write to disk
    file_info = await message.bot.get_file(file_id)
    file_path: str | None = file_info.file_path
    downloaded_file = await message.bot.download_file(file_path)
    with open(f'{file_id}.mp3', 'wb') as f:
        f.write(downloaded_file.getvalue())
    # convert file to .ogg, send it as voice message
    sound = AudioSegment.from_mp3(f'{file_id}.mp3')
    sound.export('result.ogg', format='ogg', codec="libopus")
    voice = FSInputFile('result.ogg')
    await message.answer_voice(voice=voice, duration=duration)
    # remove temp files
    os.remove('result.ogg')
    os.remove(f'{file_id}.mp3')

# Downloading audio from message
async def download_audiofile(message: Message,
                             audioname: str = None, is_voice: bool = False) -> None:
    if is_voice:
        audio = message.voice
        file_id: str = audio.file_id
        audio_name: str = audioname
    else:
        audio = message.audio
        file_id: str = audio.file_id
        audio_name: str | None = audio.file_name
    if not audio_name:
        audio_name = f'{hashlib.md5(file_id.encode()).hexdigest()}.mp3'
    file_info = await message.bot.get_file(file_id)
    file_path: str | None = file_info.file_path
    downloads_path: str = os.path.join(os.environ['USERPROFILE'], 'Downloads', audio_name)
    downloaded_file = await message.bot.download_file(file_path)
    with open(downloads_path, 'wb') as f:
        f.write(downloaded_file.getvalue())

# Handler for command /start
@router.message((F.text == '/start') & F.from_user.id.in_(whitelist))
async def start(message: Message) -> None:
    await message.answer('Glad to see you here <3')

# Handler for command /music
@router.message(F.text.contains('/music') & F.text.startswith('/')
                & F.from_user.id.in_(whitelist))
async def download_music(message: Message) -> None:
    if len(message.text) <= 7:
        await message.answer('No query provided')
        return
    query: str = message.text[7:]
    await message.answer(f'Searching for {query}')
    try:
        search_res: list[dict] = functions.yt.search(query=query, filter='videos', limit=1)
    except YTMusicUserError:
        await message.answer(f'Error while searching.')
        return
    mus_id: str = search_res[0]['videoId']
    url: str = functions.base_url + mus_id
    await functions.download_audio(url, query)
    await message.reply(f'Downloaded, sending!\n{url}')
    await message.answer_audio(audio=FSInputFile(f'{query}.mp3'))
    os.remove(f'{query}.mp3')

# Handler for audio to voice conversion
@router.message(F.audio & F.from_user.id.in_(whitelist))
async def convert_to_voice(message: Message) -> None:
    await voice_send(message)

# Download music from YouTube Music link
@router.message(F.text.contains('music.youtube.com') & F.from_user.id.in_(whitelist))
async def download_music_from_link(message: Message) -> None:
    url: str = message.text
    await message.reply('Initializing download...')
    try:
        await functions.download_audio(url)
    except (DownloadError, ExtractorError):
        await message.answer('Error while downloading/extracting audio')
        return
    await message.answer_audio(audio=FSInputFile('result.mp3'))
    os.remove('result.mp3')
