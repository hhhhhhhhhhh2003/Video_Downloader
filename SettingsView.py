import flet
import SettingsDatabase

class SettingsView:
    def __init__(self):
        self.db=SettingsDatabase.SettingsDatabase()
        self.db.create()
        self.download_path=flet.TextField(label='download path',expand=True,value=self.db.return_download_path())
        self.choose_path_button=flet.Button(
            content='选择目录',
            on_click=self.select_path
            )
        self.audio_dropdown=flet.Dropdown(
            on_select=self.audio_select,
                         text=self.db.return_audio(),
                         options=[
                             flet.DropdownOption(text='mp3'),
                             flet.DropdownOption(text='aac'),
                             flet.DropdownOption(text='wav')
                             ]
                         )
        self.video_dropdown=flet.Dropdown(
            on_select=self.video_select,
                         text=self.db.return_video(),
                         options=[
                             flet.DropdownOption(text='mp4'),
                             flet.DropdownOption(text='不指定'),
                             flet.DropdownOption(text='mov'),
                             flet.DropdownOption(text='mkv'),
                             flet.DropdownOption(text='webm')
                             ]
                         )
        self.download_video_checkbox=flet.Checkbox(
            label="下载视频",
            value=self.db.return_select_video(),
            on_change=self.db.select_video_updata
            )
        self.download_audio_checkbox=flet.Checkbox(
            label='下载音频',
            value=self.db.return_select_audio(),
            on_change=self.db.select_audio_updata
            )

    def create(self):
        return flet.Column(
            controls=[
             flet.Text(value='下载目录:',weight=flet.FontWeight.W_800,size=20),
             flet.Row(
                controls=[
                    self.download_path,
                    self.choose_path_button
                    ]
                ),
             flet.Text(value='格式选择:',weight=flet.FontWeight.W_800,size=20),
             flet.Row(
                 controls=[
                     flet.Text(value='音频格式:',size=18,weight=flet.FontWeight.W_400),
                     self.audio_dropdown,
                     flet.Text(value='视频格式:',size=18,weight=flet.FontWeight.W_400),
                     self.video_dropdown
                     ]
                 ),
             flet.Text(value='下载内容:',size=18,weight=flet.FontWeight.W_800),
             flet.Row(
                 controls=[self.download_audio_checkbox,
                 self.download_video_checkbox]
                 )
             ]
        )

    async def select_path(self,e):
        path=await flet.FilePicker().get_directory_path()
        if path!=None:
            self.download_path.value=path
            self.db.download_path_updata(path)
        self.download_path.update()

    async def audio_select(self,e):
        self.db.audio_updata(self.audio_dropdown.text)

    async def video_select(self,e):
        self.db.video_updata(self.video_dropdown.text)
