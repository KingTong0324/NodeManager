import os
import json
from collections import defaultdict

class NodeDatabase:
    def __init__(self):
        base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.nodes_dir=os.path.join(base_dir,"nodes")

        if not os.path.exists(self.nodes_dir):
            os.makedirs(self.nodes_dir)

    def get_country_file(self,country_name):
        return os.path.join(self.nodes_dir,f"{country_name}.json")

    def load_country(self,country_name):
        path=self.get_country_file(country_name)

        if not os.path.exists(path):
            return []

        try:
            with open(path,"r",encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_country(self,country_name,nodes):
        path=self.get_country_file(country_name)

        with open(path,"w",encoding="utf-8") as f:
            json.dump(nodes,f,ensure_ascii=False,indent=4)

    def add_nodes(self,nodes):
        groups={}

        for node in nodes:
            country_name=node.get("country_name","")

            if not country_name:
                continue

            if country_name not in groups:
                groups[country_name]=[]

            groups[country_name].append(node)

        for country_name,new_nodes in groups.items():
            old_nodes=self.load_country(country_name)

            all_nodes=old_nodes+new_nodes
            all_nodes=self.deduplicate(all_nodes)
            all_nodes=self.renumber(all_nodes)

            self.save_country(country_name,all_nodes)

        return self.load_all()

    def delete_node(self,ip,port):
        for file in os.listdir(self.nodes_dir):
            if not file.endswith(".json"):
                continue

            country_name=file[:-5]
            nodes=self.load_country(country_name)

            result=[]

            for node in nodes:
                if node.get("ip")==ip and node.get("port")==port:
                    continue

                result.append(node)

            result=self.renumber(result)
            self.save_country(country_name,result)

    def country_order(self):
        return {
            "中国":0,
            "香港":1,
            "台湾":2,
            "日本":3,
            "韩国":4,
            "新加坡":5,
            "美国":6,
            "澳大利亚":7,
            "加拿大":8,

            "德国":9,
            "法国":10,
            "英国":11,
            "荷兰":12,
            "瑞士":13,
            "意大利":14,
            "西班牙":15,

            "巴西":16,

            "马来西亚":17,
            "泰国":18,
            "越南":19,
            "菲律宾":20,
            "印度尼西亚":21,
            "土耳其":22,

            "瑞典":23,
            "挪威":24,
            "芬兰":25,
            "丹麦":26,
            "波兰":27,
            "奥地利":28,
            "比利时":29,
            "葡萄牙":30,
            "爱尔兰":31,
            "捷克":32,
            "俄罗斯":33,

            "墨西哥":34,

            "新西兰":35,

            "阿联酋":36,
            "以色列":37,
            "沙特":38,

            "南非":90,
            "埃及":91,
            "尼日利亚":92,

            "印度":95,

            "其他":99
        }

    def load_all(self):
        result=[]

        if not os.path.exists(self.nodes_dir):
            return result

        for file in os.listdir(self.nodes_dir):
            if not file.endswith(".json"):
                continue

            path=os.path.join(self.nodes_dir,file)

            try:
                with open(path,"r",encoding="utf-8") as f:
                    data=json.load(f)

                result.extend(data)

            except Exception:
                pass

        result=self.deduplicate(result)

        order=self.country_order()

        result.sort(
            key=lambda x:(
                order.get(
                    x.get("country_name",""),
                    99
                ),
                x.get("number","")
            )
        )

        return result

    def deduplicate(self,nodes):
        result=[]
        index={}

        for node in nodes:
            key=(
                node.get("ip",""),
                node.get("port","")
            )

            if key in index:
                result[index[key]]=node
            else:
                index[key]=len(result)
                result.append(node)

        return result

    def renumber(self,nodes):
        counters=defaultdict(int)

        for node in nodes:
            country=node.get("country_name","OTHER")

            counters[country]+=1
            node["number"]=f"{counters[country]:02d}"

        return nodes