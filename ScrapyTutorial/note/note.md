# scrapy学习笔记

## 基本操作
### 项目创建及启动
1. 新建项目 scrapy startproject xxx(项目名称)
2. 启动方式 scrapy crawl SpiderName.标识蜘蛛。它在一个项目中必须是唯一的，也就是说，不能为不同的蜘蛛设置相同的名称。
3. scrapy shell 'http://quotes.toscrape.com/page/1/' 
使用scrappy提取数据的最佳方法是使用 Scrapy shell

### 链接跟踪
```
    方法1
    next_page = response.urljoin(next_page)
    yield scrapy.Request(next_page, callback=self.parse)
    方法2
    yield response.follow(next_page, callback=self.parse)
```

### 四种常见爬虫
1. CrawlSpider 方便用于追踪链接
2. XMLFeedSpider 方便XML分析
3. CSVSpider 按行读取csv文件
4. SitemapSpider 爬取网站的sitemap信息

### 3种选择器
1. css选择器
    ![](./img/css选择器.png)
2. xpath选择器
3. 内置选择器

### Item Loader
Item提供保存抓取到数据的容器，而 Itemloader提供的是填充容器的机制。Itemloader提供的是一种灵活，高效的机制，可以更方便的被spider或source format （HTML, XML, etc）
扩展并重写，更易于维护，尤其是分析规则特别复杂繁多的时候。


注意：ItemLoader可以传递的参数有item=None, selector=None, response=None，如果是循环Selector
的时候，就可以传selector
```
for quote in response.css('div.quote'):
        quoteLoader = ItemLoader(item=QuoteItem(), selector=quote)
        quoteLoader.add_css('text', 'span.text::text')
        quoteLoader.add_css('author', 'small.author::text')
        quoteLoader.add_css('tags', 'div.tags a.tag::text')

        quoteInfo = quoteLoader.load_item()
        print(quoteInfo)
```

#### Field 字段事实上有两个参数：
1. 第一个是输入处理器（input_processor） ，当这个item，title这个字段的值传过来时，可以在传进来的值上面做一些预处理。
2. 第二个是输出处理器（output_processor） ， 当这个item，title这个字段被预处理完之后，输出前最后的一步处理。

#### scrapy内置的处理器:
1. TakeFirst: 是Scrapy提供的内置处理器，用于提取List中的第一个非空元素
2. MapCompose: 能把多个函数执行的结果按顺序组合起来，产生最终的输出，通常用于输入处理器
    ```
    # 单独直接使用
    from scrapy.loader.processors import MapCompose
    
    def add_firstStr(value):
        return value + "_firstAdd"
    
    def add_secondStr(value):
        return value + "_secondAdd"
    
    # stop_on_none=True, 指定在遇到None时，不用中断，还继续处理
    # 依次处理每个list元素
    proc = MapCompose(add_firstStr, add_secondStr, str.upper, stop_on_none=True)
    
    # 接收对象是一个可迭代的对象，如list
    result = proc(['one', 'two', 'three'])
    
    # 结果：result = ['ONE_FIRSTADD_SECONDADD', 'TWO_FIRSTADD_SECONDADD', 'THREE_FIRSTADD_SECONDADD']
    print(f"result = {result}")
    ```
3. Identity: 最简单的处理器，不进行任何处理，直接返回原来的数据。无参数
4. Join: 返回用分隔符连接后的值。分隔符默认为空格。不接受Loader contexts。
5. Compose: 用给定的多个函数的组合，来构造的处理器。list对象（注意不是指list中的元素），依次被传递到第一个函数，然后输出，
            再传递到第二个函数，一个接着一个，直到最后一个函数返回整个处理器的输出。默认情况下，当遇到None值（list中有None值）的时候
            停止处理。可以通过传递参数stop_on_none = False改变这种行为。

    
#### 每个字段的数据的处理过程是：
1. 第一步， 通过 add_xpath(), add_css() 或者 add_value() 方法)，提取到数据。
2. 第二步，将提取到的数据，传递到输入处理器（input_processor）中进行处理，处理结果被收集起来，并且保存在ItemLoader内（但尚未分配给该Item）。
3. 第三步，最后调用输出处理器（output_processor）来处理之前收集到的数据（这是最后一步对数据的处理）。然后再存入到Item中，输出处理器的结果是被分配到Item的最终值｡
4. 第四步，收集到所有的数据后, 调用ItemLoader.load_item() 方法来填充，并得到填充后的 Item 对象。

#### 重用和扩展ItemLoaders
1. 添加默认的处理机制


    即自己实现一个loader，继承原有的loader，修改其处理器
    ```
        系统itemloader的定义
        class ItemLoader(object):
            default_item_class = Item
            # 可以看到是有默认的输入/输出处理器的，而且默认是什么都不做
            default_input_processor = Identity()
            default_output_processor = Identity()
            default_selector_class = Selector
    ```
2. 重写，覆盖默认的处理机制

### Scrapy shell
有时，您希望检查在您的蜘蛛的某个点上正在处理的响应，如果只是检查您期望的响应是否到达那里的话。下面是一个案例
   ```
    import scrapy
    
    class MySpider(scrapy.Spider):
        name = "myspider"
        start_urls = [
            "http://example.com",
            "http://example.org",
            "http://example.net",
        ]
    
        def parse(self, response):
            # We want to inspect one specific response.
            if ".org" in response.url:
                from scrapy.shell import inspect_response
                inspect_response(response, self)
    
            # Rest of parsing code.
   ```
   

### 项目管道
#### 主要构成4个方法
1. process_item(self, item, spider)
    + 对每个项管道组件调用此方法。 process_item() 必须：返回包含数据的dict，返回 Item （或任何后代类）对象
2. open_spider(self, spider)
    + 当spider打开时调用此方法,只调用一次
3. close_spider(self, spider)
    + 当spider关闭时调用此方法,只调用一次
4. from_crawler(cls, crawler)
    + 不太懂
#### 项目管道的作用
+ 清理HTML数据
+ 验证抓取的数据（检查项目是否包含某些字段）
+ 检查重复项（并删除它们）
+ 爬取的项目存储在数据库中

保存到数据库的时候有两种方法，一种是同步，一种是异步操作，
详见[https://www.cnblogs.com/knighterrant/p/10783634.html]


### Feed导出
见setting.py

### 请求和响应
#### 向回调函数传递附加数据
在某些情况下，您可能对向这些回调函数传递参数感兴趣，以便稍后在第二个回调中接收这些参数

```
    def parse(self, response):
        request = scrapy.Request('http://www.example.com/index.html',
                                 callback=self.parse_page2,
                                 cb_kwargs=dict(main_url=response.url))
        request.cb_kwargs['foo'] = 'bar'  # add more arguments for the callback
        yield request

    def parse_page2(self, response, main_url, foo):
        yield dict(
            main_url=main_url,
            other_url=response.url,
            foo=foo,
        )
```
#### 使用formRequest.from_response（）模拟用户登录
```
import scrapy

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
```
#### JSONRequest

#### 响应子类
1. TextResponse
2. HtmlResponse
3. XmlResponse

### 链接提取器
链接提取器是对象，其唯一目的是从网页中提取链接 (scrapy.http.Response 对象），
最终将遵循。可以使用内置的方法从页面中提取需要的链接

### 设置


### 异常处理
1. DropItem
    + 只能在管道中使用
    + eg:raise DropItem('字段成分缺失')
2. CloseSpider
    + 可以从蜘蛛回调中引发此异常以请求关闭/停止蜘蛛
    + raise CloseSpider('关闭的原因')
3. 还有一些其他的异常：
    

## 内置服务
### 日志
#### 等级
1. logging.CRITICAL -对于严重错误（严重性最高）
2. logging.ERROR -对于常规错误
3. logging.WARNING -用于警告消息
4. logging.INFO -以获取信息性消息
5. logging.DEBUG -用于调试消息（最低严重性）
#### 日志设置
1. LOG_ENABLED = True #是否启动日志记录，默认True
2. LOG_ENCODING = 'UTF-8'
3. LOG_FILE = "log/log.log"#日志输出文件，如果为NONE，就打印到控制台
4. LOG_LEVEL = 'DEBUG'#日志级别，默认debug
5. LOG_STDOUT = False

### 统计数据集合
#### 使用
```
class ExtensionThatAccessStats(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
```
1. 设置统计值：stats.set_value('hostname', socket.gethostname())
2. 增量统计值：stats.inc_value('custom_count')
3. 获取统计值：stats.get_value('custom_count')
4. 还有很多其他的，详见文档

### 发送电子邮件
1. 使用scrapy内置的scrapy.mail或者smtp都可以
2. 可以在爬虫结束的时候进行通知
3. 通过twisted的非阻塞IO实现,可以直接写在spider中，也可以写在中间件或者扩展中

### 远程登录控制台
通过telnet远程连接查看状
### web 服务
目前官方已停止更新，下载之后不可用,

## 其他
### 实践经验
1. 分布式爬行
2. 使用user agent池
3. 禁止cookies(参考 COOKIES_ENABLED)，有些站点会使用cookies来发现爬虫的轨迹。
4. 设置下载延迟(2或更高)
5. 使用 Google cache 来爬取数据
6. 使用IP池
7. 使用高度分布式的下载器(downloader)来绕过禁止(ban)，您就只需要专注分析处理页面。
案例: http://scrapinghub.com/crawlera

