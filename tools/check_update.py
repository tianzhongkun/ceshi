import html
import json
import traceback
from urllib.parse import urlparse, parse_qs
import requests

#检查更新数据的类 利用有道云笔记 读取云笔记内容实现
"""
源码原理大概是这样的:
1.桌面新建一个文件 比如 叫 版本号.txt  然后拖到你的有道云笔记中 导入文件
2.右键这个文件 点击分享  然后将链接粘贴到浏览器上
你就会在浏览器的链接框中获取到一个链接 比如:
https://note.youdao.com/ynoteshare/index.html?id=a14dcf04d156b49ad9f3d6f3c4261a66
3.将这个id=xxx  复制这个xxx内容到下面的链接中 自己替换xxx
http://note.youdao.com/yws/public/note/xxx?editorType=0&cstk=cGtjFpHb
完整的长这样:
http://note.youdao.com/yws/public/note/a14dcf04d156b49ad9f3d6f3c4261a66?editorType=0&cstk=cGtjFpHb
4.将这个链接复制到浏览器中访问一下
大概会获得这个样子的内容:
{
    "p": "/WEB6ad8e7b39bac47b3b2827165ede2cf87",
   xxx,
   xxxx,
   xx,
}

5.里面这个 p= "xxxx"   就是你要的  记住这个
然后将这个 p  和上方的id 替换到下面的链接中
https://note.youdao.com/yws/api/personal/preview/{p}?method=convert&shareToken={id}&engine=nyozo
"""
class CheckUpdate:
    def __init__(self,var_data_url="",updatetxt_url="",netizen_teams_url=""):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"
        }
        self.var_data_url=self._parse(var_data_url)
        self.updatetxt_url=self._parse(updatetxt_url)
        self.netizen_teams_url=self._parse(netizen_teams_url)
    def get_var_data(self):
        try:
            res=requests.get(self.var_data_url,headers=self.headers)
            if res.status_code==200:
                return html.unescape(res.text).split("<pre>")[-1].split("</pre>")[0].split("\n")[:-1]
            else:
                return False
        except:
            print("请不要开梯子")
            return False
    def get_updatetxt(self):
        try:
            res = requests.get(self.updatetxt_url,headers=self.headers)
            if res.status_code == 200:
                return html.unescape(res.text).split("<pre>")[-1].split("</pre>")[0][:-1]
            else:
                return ""
        except:
            print("无法获取更新日志,请不要开梯子!")
            return ""
    def get_updatetxt(self):
        try:
            res = requests.get(self.updatetxt_url,headers=self.headers)
            if res.status_code == 200:
                return html.unescape(res.text).split("<pre>")[-1].split("</pre>")[0][:-1]
            else:
                return ""
        except:
            print("无法获取更新日志,请不要开梯子!")
            return ""
    def get_netizen_teams(self):
        try:
            res = requests.get(self.netizen_teams_url,headers=self.headers)
            if res.status_code == 200:
                return json.loads(html.unescape(res.text).split("<pre>")[-1].split("</pre>")[0][:-1])
            else:
                return []
        except:
            print("无法获取网友分享的阵容资料")
            return []
    def _parse(self,url=""):
        if url=="":
            return ""
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)  # 自动解析为字典
            id=query_params['id'][0]
            url=f"http://note.youdao.com/yws/public/note/{id}?editorType=0&cstk=cGtjFpHb"
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                p=res.json()['p']
                return f"https://note.youdao.com/yws/api/personal/preview{p}?method=convert&shareToken={id}&engine=nyozo"
            return ""
        except :
            print(f"解析直链发生异常: {traceback.format_exc()}")
if __name__ == '__main__':
    #用法例子
    jcu=CheckUpdate("https://note.youdao.com/ynoteshare/index.html?id=a14dcf04d156b49ad9f3d6f3c4261a66",
                    "https://note.youdao.com/ynoteshare/index.html?id=be350afdbe60ba9f2642be96c48476ed",
                    "https://share.note.youdao.com/ynoteshare/index.html?id=2cb8bfc79fdfb0e5e949281fb102f235"
                    )

    print(jcu.get_var_data())
    print(jcu.get_updatetxt())
    print(jcu.get_netizen_teams())
