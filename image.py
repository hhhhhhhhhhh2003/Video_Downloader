import language
import flet
import ytdlp
import os
import functools
import asyncio

def format_duration(seconds):
    seconds=int(seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}"

        self.table_container = flet.Column(scroll=flet.ScrollMode.AUTO, expand=True)
        self.prompt_word=flet.TextField(label=language.Prompt_word)
        self.download_catalog=flet.TextField(label=language.Download_catalog)
        self.download_catalog.value=os.path.join(os.path.expanduser('~'),"Downloads")

        self.progress_bar=flet.ProgressBar(width=400,visible=False)
        self.progress_text=flet.Text("准备中",visible=False)
        self.file_picker=flet.FilePicker()
        self.file_picker.path=self.download_catalog.value
        self.page.title=language.Software_name
        self.parse_button=flet.Button(content=language.Parse,on_click=self.parse_button_actions)
        self.download_button=flet.Button(content=language.Download,on_click=self.download_selected)
        self.page.on_route_change=self.main_page
        self.page.on_view_pop=self.view_pop


    async def jump_settings(self):
        await self.page.push_route("/settings")

    async def select_path(self,e):

        if(o!=None):
            self.download_catalog.value = o
        self.file_picker.path=self.download_catalog.value


    async def parse_button_actions(self):
            self.parse_button.disabled=True
            self.download_button.disabled=True
            self.parse_button.update()
            self.download_button.update()

            rows=[]
            for item in inventory_items:
                rows.append(
                    flet.DataRow(
                        selected=False,
                        on_select_change=lambda e: setattr(e.control, 'selected', e.data),
                        cells=[
                            flet.DataCell(flet.Text(str(item.get('id','')))),
                            flet.DataCell(flet.Text(str(item.get('title','无标题')))),
                            flet.DataCell(flet.Text(format_duration(item.get('duration',0)))),
                            flet.DataCell(flet.Text(item.get('url',''))),
                        ]
                    )
                )
            DataColumn=flet.DataTable(
                expand=True,
                show_checkbox_column=True,
                columns=[
                flet.DataColumn(flet.Text(language.Serial_number)),
                flet.DataColumn(flet.Text(language.Sheet_title)),
                flet.DataColumn(flet.Text(language.Sheet_duration)),
                flet.DataColumn(flet.Text(language.Link)),
                ],
            rows=rows
        )   
            self.table_container.controls.clear()
            self.table_container.controls.append(DataColumn)
            self.page.update()
            self.parse_button.disabled=False
            self.download_button.disabled=False
            self.parse_button.update()
            self.download_button.update()


        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                if total:
                    percent = d['downloaded_bytes'] / total * 100
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    asyncio.run_coroutine_threadsafe(
                        self.update_progress(percent,speed,eta),
                        loop=loop
                        )
                elif d['status'] == 'finished':
                    asyncio.run_coroutine_threadsafe(
                        self.finish_download(),
                        loop=loop
                        )
        return hook

    async def update_progress(self,percent, speed, eta):
        self.progress_bar.value = percent / 100
        self.progress_bar.visible = True
        if speed:
            speed_str = f"{speed/1024:.1f} KB/s" if speed < 1024*1024 else f"{speed/1024/1024:.1f} MB/s"
        else:
           speed_str = "未知"
        self.progress_text.value = f"下载中... {percent:.1f}% | 速度: {speed_str} | 剩余: {format_duration(eta)}"
        self.progress_text.visible = True
        self.progress_bar.update()
        self.progress_text.update()

    async def finish_download(self):
        self.progress_bar.visible = False
        self.progress_text.visible = False
        self.progress_text.update()
        self.progress_bar.update()

    async def download_selected(self,e):
        try:
            table=self.table_container.controls[0]
        except:
           return
        self.parse_button.disabled=True
        self.download_button.disabled=True
        self.parse_button.update()
        self.download_button.update()

        self.parse_button.disabled=False
        self.download_button.disabled=False
        self.parse_button.update()
        self.download_button.update()
        self.progress_bar.visible = False
        self.progress_text.visible = False
        self.progress_bar.update()
        self.progress_text.update()

    def main_page(self):
        self.page.views.clear()
        self.page.views.append(
            flet.View(
                route="/",
                controls=[
                    flet.AppBar(title=flet.Text(language.Main_page)),
                    flet.Button(language.Set, on_click=self.jump_settings),
                    flet.Text(language.Prompt_statement1),
                    flet.Row(
                        controls=[
                            self.prompt_word,
                            self.parse_button,
                            self.download_button
                            ],
                        ),
                    self.table_container,
                    flet.Column([self.progress_bar,self.progress_text])
                    ]
                )
            )
        if(self.page.route=='/settings'):
            self.page.views.append(
                flet.View(
                    route="/settings",
                    controls=[
                        flet.AppBar(
                            title=flet.Text(language.Set),

                        ]
                    )
                )
            self.page.update()
        self.page.update()

    async def view_pop(self,e):
        if e.view is not None:
            self.page.views.remove(e.view)
            top_view=self.page.views[-1]
            await self.page.push_route(top_view.route)
