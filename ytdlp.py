import yt_dlp
import sys
import os

def exception_handling(e):
    if isinstance(e,yt_dlp.utils.UnsupportedError):
        return f"不支持的网站:{e}"
    elif isinstance(e,yt_dlp.utils.LockingUnsupportedError):
        return f"文件锁定:{e}"
    elif isinstance(e,yt_dlp.utils.GeoRestrictedError):
        return f"地域限制:{e}"
    elif isinstance(e,yt_dlp.utils.ExtractorError):
        return f"提取器错误:{e}"
    elif isinstance(e,yt_dlp.utils.PostProcessingError):
        return f"ffmpeg错误:{e}"
    elif isinstance(e,yt_dlp.utils.DownloadError):
        return f"下载错误:{e}"
    elif isinstance(e,yt_dlp.utils.UnavailableVideoError):
        return f"视频不可用:{e}"
    elif isinstance(e,AttributeError):
        return f"属性错误:{e}"
    elif isinstance(e,TypeError):
        return f"类型错误:{e}"
    else:
        return f"未知错误:{e}"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if os.name=='nt':
    ffmpeg_dependencies=resource_path(os.path.join('ffmpeg','bin', 'ffmpeg.exe'))
else:
    ffmpeg_dependencies=None

class DownloadOperate:
    def __init__(
        self,
        bestvideo,
        bestaudio,
        coding,
        subtitle,
        download_path,
        preferredformat=None,
        subtitle_format='srt/ass/best'
        ):
        self.ydl_opts={
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_dependencies,
            'subtitlesformat':subtitle_format,
            'no_color': True,
            'writesubtitles':subtitle,
            'keepvideo':False
            }
        format_parts = []
        if bestvideo:
            format_parts.append('bestvideo')
        if bestaudio:
            format_parts.append('bestaudio')
        if format_parts:
            self.ydl_opts['format'] = '+'.join(format_parts)
        else:
            self.ydl_opts['format'] = 'best'
        if bestaudio and not bestvideo:
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': coding,
            }]
        elif bestvideo and preferredformat:
            self.ydl_opts['postprocessors']=[{
                'key':'FFmpegVideoConvertor',
                'preferedformat':preferredformat
                }]
        self.error=None

    def download_operate(self,progress_callback,url):
        try:
            self.ydl_opts['progress_hooks']=[progress_callback]
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            self.error=exception_handling(e)
            return False

class ParsingOperations:
    def __init__(self,url):
        self.url=url
        self.video_list=[]
        self.info=None
        self.error=None

    def is_it_valid(self):
        ydl_opts={
            'quiet':True,
            'extract_flat':True,
            'no_color': True
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.info=ydl.extract_info(self.url,download=False)
                return True
        except Exception as e:
            self.error=exception_handling(e)
            return False

    def parse_playlist(self):
        try:
            e=self.is_it_valid()
            if e==False:
                return False
            entries=self.info.get('entries',[self.info])
            for i,entry in enumerate(entries,start=1):
                self.video_list.append({
                    'id':i,
                    'title':entry.get('title','ccc'),
                    'duration':entry.get('duration',0),
                    'url':entry.get('webpage_url') or entry.get('url') 
                    })
            return self.video_list
        except Exception as e:
            self.error=exception_handling(e)
            return False
