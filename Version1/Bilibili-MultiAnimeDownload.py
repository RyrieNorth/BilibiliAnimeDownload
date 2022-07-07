##用前说明：
##这个小脚本目前只支持下载epid类型的番剧

##加载基本库
import requests
import json
import os
import sys
from urllib import parse

##定义视频Ep号
VideoEp = "567947"          ##在这里填入视频的Ep号，这里使用新 东京猫猫 做测试

##定义清晰度
VideoHD = "80"             ##在这里选择视频的BV号，这里使用80，视频清晰度可以下图表查看
#| 值   | 含义              ##注意：越高清晰度的视频需要登陆，不登陆的视频清晰度为720P
#| ---- | --------------
#| 6    | 240P 极速     
#| 16   | 360P 流畅
#| 32   | 480P 清晰
#| 64   | 720P 高清
#| 74   | 720P60 高帧率
#| 80   | 1080P 高清
#| 112  | 1080P+ 高码率
#| 116  | 1080P60 高帧率
#| 120  | 4K 超清
#| 125  | HDR 真彩色
#| 126  | 杜比视界
#| 127  | 8K 超高清

##定义视频流
VideoType = "0"             ##在这里选择视频的二进制流格式，这里使用0(flv)，视频流设置可以在下图表查看
#| 值   | 含义               ##如果这里使用1则会返回360p的视频，我都服了
#| ---- | ------------------
#| 0    | flv格式
#| 1    | mp4格式
#| 16   | dash格式
#| 64   | 是否需求 HDR 视频
#| 128  | 是否需求 4K 分辨率
#| 256  | 是否需求杜比音频
#| 512  | 是否需求杜比视界
#| 1024 | 是否需求 8K 分辨率
#| 2048 | 是否需求 av1 编码

##账号Cookies，这里填的是你登陆B站后获取的Cookies值，该值用于下载更高清晰度的视频
##获取完Cookies后请千万不能泄露！！！有了Cookies之后就能直接对账号进行操作，所以请千万要保管好！！！
Cookies = 'SESSDATA='

##切换当前目录
os.chdir(sys.path[0])

##在当前目录创建Video文件夹用于存放下载的视频，当然你也可以手动指定
Path = os.getcwd()
VideoPath = (Path + '\\Video')
if not os.path.exists(VideoPath):
    os.makedirs(VideoPath)

##构造请求头部，告诉B站我不是机器人
headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0",
    "content-type": "application/json; charset=utf-8",
    "Referer": "https://www.bilibili.com",
    "Cookie": f"{Cookies}"
}

##Bilibili播放器的API，用于获取视频的Cid
apiurl = "http://api.bilibili.com/x/player/playurl?&"

##Bilibili动画的API，用于获取番剧的Bv号
AnimeListURL = f"http://api.bilibili.com/pgc/view/web/season?" + "ep_id=" + VideoEp

##获取番剧的Bv号
AnimeRes = requests.get(url=AnimeListURL,headers=headers)
Animejs = json.loads(AnimeRes.text)
Animejs1 = (Animejs.get("result"))
Animejs2 = (Animejs1.get("episodes"))

for i in Animejs2:
    AnimeID = (i.get("bvid"))
    AnimeName = (i.get("share_copy")).replace(" ","-")

    ##获取视频/视频合集的cid、标题
    VideoListURL = f"https://api.bilibili.com/x/player/pagelist?bvid={AnimeID}&jsonp=jsonp"

    ##获取视频Cid
    VideoRes = requests.get(url=VideoListURL,headers=headers)
    Videojs = json.loads(VideoRes.text)
    for i in Videojs.get('data'):
        VideoCid = (i.get('cid'))
        VidelTitle = (i.get('part')).replace(" ","-")
    ##构造请求参数
        payload = {
            "bvid": f"{AnimeID}",           ##这里就是视频的Bv号，别问我为什么没有Av，因为我懒得弄了
            "cid": f"{VideoCid}",           ##这里是视频/视频列表的cid号，这里用于标识视频的URL位置
            "qn": f"{VideoHD}",             ##这里是视频的清晰读选择，详情请查看
            "fnval": f"{VideoType}",        ##这里是设置视频的二进制流格式
            "fnver": "0",                   ##目前该值恒为0，即`fnver=0`
            "fourk": "1"                   ##是否允许4K视频，默认为0，画质最高1080P：0，画质最高4K：1
}
        ##对请求参数进行编码
        data = parse.urlencode(payload)

        ##重构URL地址，并请求
        resurl = apiurl + data
        res = requests.get(url=resurl,headers=headers).text

        ##获取视频地址，并将对应标题对应输出
        js1 = json.loads(res)
        js2 = (js1.get('data'))             ##这里别问我为什么写成这个样子，因为我只是个小白，我实在想不出有什么好方法了……
        js3 = (js2.get('durl'))

        for x in js3:
            URL = (x.get('url'))
            
            ##构建aria2下载参数，并使用python调用
            aria2_path = r".\tools\aria2c\aria2c.exe"
            order1 = aria2_path + ' -s32 -x16 --referer="https://www.bilibili.com"' + ' ' f'"{URL}"' + ' ' + '-o ' + '.\Video\\' f'{AnimeName}.flv'
            os.system(order1)
            print ("下载完成！！！")