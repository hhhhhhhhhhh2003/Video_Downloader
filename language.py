
Prompt_statement1="请在下方输入链接："
Prompt_word="视频url"
Sheet_title="标题"
Sheet_duration="时长"
Download_catalog="下载目录"
Select_all="全选"
Parse="解析"
Title_format="标题格式"
Download_content="下载内容"
Audio="音频"
Video="视频"
Subtitle="字幕"
Download='下载'
Software_name="视频下载器"
Set='设置'
Main_page='主页面'
Serial_number="序号"
Link="链接"
def Read_configuration():
    try:
        with open("language.txt",'r',encoding='utf-8') as f:
            lines=[line.strip()for line in f if line.strip()]
            if len(lines)<13:
                return None
            return lines
    except FileNotFoundError:
        return None
