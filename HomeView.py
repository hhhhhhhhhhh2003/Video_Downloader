import flet
import crawl

class HomeView:
    def __init__(self, download_view):
        self.url_field=flet.TextField(label='url',expand=True)
        self.download_view=download_view
        self.analysis_button=flet.Button(
            content='解析',
            on_click=self.analysis
            )
        self.download_button=flet.Button(
            content='下载',
            on_click=self.download
            )
        self.data_table=flet.DataTable(
            show_checkbox_column=True,
            expand=True,
            columns=[
                flet.DataColumn(label=flet.Text('id')),
                flet.DataColumn(label=flet.Text('title')),
                flet.DataColumn(label=flet.Text('duration')),
                flet.DataColumn(label=flet.Text('URL'))
                ],
            rows=[]
            )

    def create(self):
        return flet.Column(
            controls=[
                flet.Row(
                controls=[
                    self.url_field,
                    self.analysis_button,
                    self.download_button
                    ]
                ),
                self.data_table
            ]
        )

    def analysis(self):
        rows=[]
        url=self.url_field.value

        def on_dropdown(e):
            e.control.selected=e.data

        for i in crawl.Analysis().parse_playlist(url):
            video_duration=i.get('duration')
            if video_duration is None:
                video_duration=0
            rows.append(
                flet.DataRow(
                    on_select_change=on_dropdown,
                    expand=True,
                    cells=[
                        flet.DataCell(content=flet.Text(i.get('id',''))),
                        flet.DataCell(flet.Text(i.get('title','无标题'))),
                        flet.DataCell(flet.Text(f"{int(video_duration//60//60)}:{int(video_duration//60%60)}:{int(video_duration%60)}")),
                        flet.DataCell(flet.Text(i.get('url',''))),
                        ]
                    )
                )
        self.data_table.rows=rows
        self.data_table.update()

    def download(self):
        rows=[]
        for i in self.data_table.rows:
            if i.selected:
                row : flet.Text = i.cells[0].content
                rows.append(
                    (row.value,i.cells[1].content,i.cells[3].content.value)
                    )
        self.download_view.add(rows)
        