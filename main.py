import flet
import MainView

def main(page:flet.Page):
    view=MainView.MainView(page)
    view.create()
    page.title='视频下载器'

if __name__ == '__main__':
    flet.run(main)