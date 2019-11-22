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
