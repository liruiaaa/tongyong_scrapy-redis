# tongyong_scrapy-redis
一个通用的scrapy-redis已经配置完挂好布隆过滤器代理中间件请求头中间件  
scrapy-redis需要先推入url我写在初始化方法中正常运行就可以  
要写入es先运行models的文件  
scrapy-redis主要是和进行分布式和断点续爬去重  
存储是异步存入mysql有需要自己更改吧pipeline注释打开就可以  
里面配置存到elasticsearch中的方法分局需要自己改  
可以运行scrapy crawlall运行全部爬虫把setting注释打开就可以  
如果需要运行单个配置在main文件下把crawl后面的改成要运行的spider名  

