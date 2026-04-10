import yt_dlp
import SettingsDatabase
import os
class Analysis:
    def __init__(self):
        self.ydl_opts={}

    def parse_playlist(self,url):
        video_list=[]
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info=ydl.extract_info(url,download=False)
                entries=info.get('entries',[info])
                for i,entry in enumerate(entries,start=1):
                    video_list.append(
                    {
                        'id':i,
                        'title':entry.get('title','ccc'),
                        'duration':entry.get('duration',0),
                        'url':entry.get('webpage_url')
                        }
                    )
                return video_list
            except:
                return []

class download:
    def __init__(self):
        self.ydl_opts=Analysis().ydl_opts

    def download(
        self,
        url,
        title,
        progress_callback=None
        ):
        db=SettingsDatabase.SettingsDatabase()
        if db.return_select_audio() and db.return_select_video():
            self.ydl_opts['format']='bestvideo+bestaudio/best'
            video=db.return_video()
            if video!= '不指定':
                self.ydl_opts['merge_output_format']=video
        elif db.return_select_video():
            video=db.return_video()
            self.ydl_opts['format']='bestvideo'
            if video!= '不指定':
                self.ydl_opts['merge_output_format']=video
        elif db.return_select_audio():
            self.ydl_opts['format']='bestaudio/best'
            self.ydl_opts['postprocessors']=[{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': db.return_audio(),
}]
        else:
            self.ydl_opts['format']='best'
        self.ydl_opts['outtmpl']=f'{db.return_download_path()}/{title}.%(ext)s'
        self.ydl_opts['progress_hooks']=[progress_callback]
        if os.name == 'nt':
            self.ydl_opts['ffmpeg_location']=os.path.join('ffmpeg','bin','ffmpeg.exe')
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([url])
            except:
                pass
            
