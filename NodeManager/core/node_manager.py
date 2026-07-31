from core.storage import NodeStorage
from core.node_database import NodeDatabase
from collections import defaultdict

class NodeManager:
    def __init__(self):
        self.storage = NodeStorage()
        self.database = NodeDatabase()
        self.current_nodes = []
        self.saved_nodes = []
        self.load_database()

    def set_current(self, nodes):
        self.current_nodes = nodes
        return self.current_nodes

    def get_current(self):
        return self.current_nodes

    def add_to_saved(self, nodes):
        data = []

        for node in nodes:
            data.append(node.to_dict())

        self.database.add_nodes(data)
        self.load_database()

        return self.saved_nodes

    def get_saved(self):
        return self.saved_nodes

    def delete(self, ip, port):
        self.database.delete_node(ip, port)
        self.load_database()

        return self.saved_nodes

    def renumber(self):
        counters = defaultdict(int)

        for node in self.saved_nodes:
            country = node.country or "OTHER"
            counters[country] += 1
            node.number = f"{counters[country]:02d}"

    def clear_current(self):
        self.current_nodes = []

    def clear_saved(self):
        self.saved_nodes = []

    def load_database(self):
        data = self.database.load_all()
        self.saved_nodes = []

        from core.node_model import Node

        for item in data:
            node = Node()
            node.from_dict(item)
            self.saved_nodes.append(node)

        return self.saved_nodes

    def format_nodes(self, nodes):
        result = []

        for node in nodes:
            result.append(node.output_line())

        return "\n".join(result)