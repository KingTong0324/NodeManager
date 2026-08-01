import os
import json
from collections import defaultdict

from core.node_model import Node



class NodeStorage:
    """
    节点存储管理

    功能：

    1. 保存节点文件
    2. 加载节点文件
    3. 节点去重
    4. 自动编号
    """



    def save_file(
        self,
        path,
        nodes
    ):
        """
        保存节点到指定文件

        path:
            用户选择的json文件

        nodes:
            Node列表
        """


        data = []


        for node in nodes:

            data.append(
                node.to_dict()
            )



        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )



        return True




    def load_file(
        self,
        path
    ):
        """
        从JSON文件加载节点
        """


        if not os.path.exists(
            path
        ):

            return []



        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(
                f
            )



        nodes = []



        for item in data:

            node = Node()

            node.from_dict(
                item
            )

            nodes.append(
                node
            )



        return nodes




    def merge(
        self,
        old_nodes,
        new_nodes
    ):
        """
        合并节点

        根据:
        IP + 端口

        去重
        """


        result = []

        exists = set()



        for node in (
            old_nodes + new_nodes
        ):


            key = (
                node.ip,
                node.port
            )


            if key in exists:

                continue



            exists.add(
                key
            )


            result.append(
                node
            )



        return self.renumber(
            result
        )




    def renumber(
        self,
        nodes
    ):
        """
        按国家重新编号

        JP:
        01
        02

        US:
        01
        02
        """



        counters = defaultdict(
            int
        )



        for node in nodes:


            country = node.country


            if not country:

                country = "OTHER"



            counters[country] += 1



            node.number = (
                f"{counters[country]:02d}"
            )



        return nodes