import yt_dlp
import json
import sys
import os
p=os.path.join(os.path.expanduser('~'),"Downloads")
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def Download_operate(
    bestvideo,#是否下载视频
    bestaudio,#是否下载音频
    coding,#编码方式
    subtitle,#是否下载字幕
    url,
    download_path=p,#下载路径
    ):
    ydl_opts={
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'ffmpeg_location': resource_path(os.path.join('ffmpeg','bin', 'ffmpeg.exe')),
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
            'preferredcodec': coding,  # 如 'mp3', 'm4a'
        }]
    ydl_opts.update({
    'writesubtitles': subtitle,
    'allsubtitles': subtitle,    
    'writeautomaticsub': subtitle
})
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def Parsing_operations(url):
    """
    解析 URL（支持单个视频或播放列表），
    返回统一格式：[{"id": 1, "title": "...", "duration": 0, "url": "..."}, ...]
    """
    ydl_opts = {}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 提取信息，不进行下载
        info = ydl.extract_info(url, download=False)
        info_json=json.dumps(ydl.sanitize_info(info))
        
        # 统一处理：如果是播放列表，'entries' 包含所有视频；
        # 如果是单个视频，info 本身就是该视频对象，将其封装进列表。
        entries = info.get('entries', [info])
        
        results = []
        # 使用 enumerate 从 1 开始编号
        for i, entry in enumerate(entries, start=1):
            results.append({
                "id": i,
                "title": entry.get('title', 'Unknown Title'),
                "duration": entry.get('duration', 0),
                "url": entry.get('webpage_url') or entry.get('url')
            })
            
        return results