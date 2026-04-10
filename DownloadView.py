import time
import flet
import threading
import crawl
import asyncio
class DownloadView:
    def __init__(self,page):
        self.page=page
        self.list_view=flet.ListView(
            controls=[],
            expand=True
            )
        self.size=5
        self.rows=[]
        threading.Thread(target=self.downloading).start()

    class ListView:
        def __init__(self,title,url,listview,page):
            self.title=flet.Text(value=title)
            self.update_time = 0
            self.page=page
            self.progress_bar=flet.ProgressBar(expand=True)
            self.url=url
            self.e=False
            self.button=flet.Button(content='取消',on_click=self.on_click)
            self.listview=listview
            self.i=True

        def on_click(self,e):
            self.e=True
            i= flet.Row(
                    controls=[
                        self.title,
                        self.progress_bar,
                        self.button
                        ]
                    )
            if i in self.listview.controls:
                self.listview.controls.remove(
                flet.Row(
                    controls=[
                        self.title,
                        self.progress_bar,
                        self.button
                        ]
                    )
                )

        def hook(self,d):
            if self.e:
                raise
            if d['status']=='downloading':
                curr_time=time.time()
                if curr_time-self.update_time>2:
                    total=d.get('total_bytes')
                    percent=d['downloaded_bytes']/total*100
                    self.progress_bar.value=percent/100
                    self.update_time=time.time()
                    print(1)

    def create(self):
        return flet.Column(
            controls=[
                flet.Text(value='下载列表:',weight=flet.FontWeight.W_800,size=20),
                self.list_view
                ]
            )

    def add(self,rows):
        row=[]
        for i in rows:
            new_list=self.ListView(f'{i[0]}-'+i[1].value,i[2],self.list_view,self.page)
            self.rows.append(new_list)
            row.append(
                flet.Row(
                    controls=[
                        new_list.title,
                        new_list.progress_bar,
                        new_list.button
                        ]
                    )
                )
        self.list_view.controls.extend(row)

    def downloading(self):
        while True:
            leng=threading.active_count()
            if leng<self.size:
                threading.Thread(target=self.download).start()

    def download(self):
        for i in self.rows:
            if i.i:
                i.i=False
                crawl.download().download(i.url,i.title.value,i.hook)
                i.on_click(None)
                break

