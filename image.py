from re import S
import language
import flet as ft
import flet
import ytdlp

def format_duration(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        else:
            return f"{m}:{s:02d}"

def Main_page(page:flet.Page):
    table_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    page.scroll = ft.ScrollMode.AUTO
    page.title=language.Software_name
    Prompt_word=flet.TextField(label=language.Prompt_word)
    async def Jump_settings():
        await page.push_route("/settings")
    async def Parse_button_actions():
        inventory_items=ytdlp.Parsing_operations(Prompt_word.value)
        rows=[]
        def handle_row_selection(e):
            e.control.selected = e.data  # 更新当前行的选中状态
            e.control.update()
        for item in inventory_items:
            rows.append(
                ft.DataRow(
                    selected=False,
                    on_select_change=handle_row_selection,
                    cells=[
                        flet.DataCell(flet.Text(str(item.get('id','')))),
                        flet.DataCell(flet.Text(str(item.get('title','无标题')))),
                        flet.DataCell(flet.Text(format_duration(item.get('duration',0)))),
                        flet.DataCell(flet.Text(item.get('url',''))),
                        ]
                    )
                )
        DataColumn=\
            flet.DataTable(
            expand=True,
            show_checkbox_column=True,
            columns=[
                flet.DataColumn(flet.Text(language.Serial_number)),
                ft.DataColumn(ft.Text(language.Sheet_title)),
                ft.DataColumn(ft.Text(language.Sheet_duration),numeric=True),
                ft.DataColumn(flet.Text(language.Link)),
                ],
            rows=rows
        )
        table_container.controls.clear()
        table_container.controls.append(DataColumn)
        page.update()
    
    async def Download_selected(e):
        table=table_container.controls[0]
        selected_urls=[]
        for row in table.rows:
            if(row.selected):
                url_cell=row.cells[3].content
                if isinstance(url_cell,ft.Text):
                    url=url_cell.value
                    selected_urls.append(url)
        page.update()

        def download_task():
            for url in selected_urls:
                ytdlp.Download_operate(
                    download_path=r"C:\Users\hhhhh\Downloads",  # 可改为配置或变量
                    bestvideo=True,
                    bestaudio=True,
                    coding='m4a',      # 仅下载音频时有效，这里保留不影响
                    subtitle=True,
                    url=url
                    )
                print(f"{url}")
        download_task()
    def Main_page():
        page.views.clear()
        page.views.append(
            flet.View(
                route="/",
                controls=[
                    flet.AppBar(title=flet.Text(language.Main_page)),
                    flet.Button(language.Set,on_click=Jump_settings),
                    flet.Text(language.Prompt_statement1),
                    flet.Row(
                        controls=[
                            Prompt_word,
                            flet.Button(content=language.Parse,on_click=Parse_button_actions),
                            flet.Button(content=language.Download,on_click=Download_selected)
                            ],
                        ),
                    table_container
                    ]
                )
            )
        if(page.route=='/settings'):
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[
                        flet.AppBar(
                            title=ft.Text(language.Set),
                            ),
                        ]
                    )
                )
            page.update()
        page.update()
    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view=page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change=Main_page
    page.on_view_pop=view_pop

    Main_page()