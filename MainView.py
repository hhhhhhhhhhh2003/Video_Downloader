import flet
import SettingsView
import HomeView
import DownloadView
class MainView:
    def __init__(self,page:flet.Page):
        self.page=page
        self.download_view=DownloadView.DownloadView(page)
        self.home_view=HomeView.HomeView(self.download_view)
        self.settings_view=SettingsView.SettingsView()
        self.tabs=flet.Tabs(
            selected_index=0,
            length=3,
            expand=True,
            content=flet.Column(
                expand=True,
                controls=[
                    flet.TabBar(
                        tabs=[
                            flet.Tab(label='Home',icon=flet.Icons.HOME),
                            flet.Tab(label='Settings',icon=flet.Icons.SETTINGS),
                            flet.Tab(label='Download',icon=flet.Icons.DOWNLOAD),
                            ]
                        ),
                    flet.TabBarView(
                        expand=True,
                        controls=[self.home_view.create(),self.settings_view.create(),self.download_view.create()]
                        ),
                    ]
                )
            )

    def create(self):
        self.page.add(self.tabs)
        self.tabs.update()
