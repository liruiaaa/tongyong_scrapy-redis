from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

# 导入连接elasticsearch(搜索引擎)服务器方法
connections.create_connection(hosts=['IP地址'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
class TongyongwenzhangType(DocType):  # 自定义一个类来继承DocType类
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")#需要分析text()
    content = Text(analyzer="ik_max_word")
    gtime =Date()
    url = Keyword()
    author = Keyword()
    ctime = Date()
    read_num = Integer()
    site_name = Keyword()

    class Meta:
        index = "wenzhang"
        doc_type = 'article'


if __name__ == "__main__":
    TongyongwenzhangType.init()