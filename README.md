# UrbanManageFine 上海市城管行政罚款爬虫
Web crawlers for the urban management fine in Shanghai 

> 上海市城市管理行政执法局行政处罚信息公开：http://183.194.249.79/web/default.aspx

> 浦东城管：http://183.194.249.79/web/search.aspx?keyword=&type=1&organ=b2327449-70d8-4478-9fc5-d6aa497b3b88

### Basic Idea
1. 不同区城管对应的网页URL是固定的，但该网页是动态网页，由javascript渲染。进行翻页操作后网页URL并不会改变，因此需要Selenium + Scrapy进行爬取。
2. 网页加载和Javascript渲染速度很慢，翻页之后渲染也很慢（通常需要30-60秒），请耐心等待。
3. 每一条罚款案件对应的子网页URL是固定的，在爬取完目录之后进入子网页爬取每条案件的细节信息。
4. 主网页（包含所有条目）和子网页使用两个不同的浏览器（前者使用Safari，后者使用chrome），使得子网页的爬取不影响主网页。


### Requirements
- `bs4`
- `selenium`
- `scrapy`

### Usage
1. 将本项目克隆在本地：`git@github.com:AstroJacobLi/UrbanManageFine.git` 之后进入`./UrbanManageFine`文件夹。请检查`./UrbanManageFine/chromedriver`是否存在。
2. 进入`./UrbanManageFine/shfine`，在该文件夹下执行：
    ```
    scrapy crawl shfine -a district='pudong' -a max_page=3 -o pudong.csv -L WARNING
    ```
    - `shfine` 代表"shanghai fine"
    - `-a district='pudong'`：获取浦东区城管处罚信息
    - `-a max_page=3`: 只爬取前三页
    - `-o pudong.csv`: 将爬取的信息保存为`pudong.csv`.
    - `-L WARNING`: 只显示级别为WARNING及以上的提示信息（scrapy废话太多了。。。）
3. 爬虫结果样例请见[`jingAn.csv`](https://github.com/AstroJacobLi/UrbanManageFine/blob/main/jingAn.csv).

```diff
- 注意！本项目仅支持MacOS！其他系统请自行更换`middelware.py`中的浏览器设置！
```

## Acknowledgement
本项目受到以下文章的启发，在此表示感谢！
1. https://blog.csdn.net/qq_43004728/article/details/84636468
2. https://www.pluralsight.com/guides/advanced-web-scraping-tactics-python-playbook
3. https://www.cnblogs.com/miners/p/9049498.html

**Author: [Jiaxuan Li](mailto:jiaxuanl@princeton.edu)**

Feel free to raise issues and report bugs!