# BilibiliAnimeDownload
Version1：目前只能下载EP号的番剧
---
Version2：目前只能下载除港澳台以外的番剧，剔除了一些无用的代码，新增了正则表达式用以判断番剧ID类型与特殊字符处理
---
感谢SocialSisterYi大佬整合的B站APi合集
https://github.com/SocialSisterYi/bilibili-API-collect
---
本次项目的核心思想在于：
---
通过某一集番剧的ID获取到整个番剧列表——通过番剧列表查询番剧Bv号——通过播放器获取到源视频地址
---
最后再用aria2下载，用FFMpeg从FLV转为MP4
---
Version1就不要再用了，试试全新的Version2吧！！！
