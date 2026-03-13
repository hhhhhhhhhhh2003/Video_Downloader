import yt_dlp
import json
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def download_operate(
    bestvideo,
    bestaudio,
    coding,
    subtitle,
    url,
    download_path,
    progress_callback=None
    ):
    ydl_opts={
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'ffmpeg_location': resource_path(os.path.join('ffmpeg','bin', 'ffmpeg.exe')),
        'subtitlesformat':'srt/ass/best'
        }
    format_parts = []
    if bestvideo:
       format_parts.append('bestvideo')
    if bestaudio:
        format_parts.append('bestaudio')
    if format_parts:
        ydl_opts['format'] = '+'.join(format_parts)
    else:
        ydl_opts['format'] = 'best'
    if bestaudio and not bestvideo:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': coding,
        }]
    ydl_opts.update({
    'writesubtitles': subtitle,   
})
    if progress_callback:
        ydl_opts['progress_hooks']=[progress_callback]
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        return

def Parsing_operations(url):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info_json=json.dumps(ydl.sanitize_info(info))
            entries = info.get('entries', [info])
            results = []
            for i, entry in enumerate(entries, start=1):
                results.append({
                    "id": i,
                    "title": entry.get('title', 'Unknown Title'),
                    "duration": entry.get('duration', 0),
                    "url": entry.get('webpage_url') or entry.get('url')
                })
            return results
    except:
        return []