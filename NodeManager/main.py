import sys
from collections import defaultdict
from PySide6.QtWidgets import QApplication, QListWidgetItem, QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QTimer
from core.converter import NodeConverter
from core.node_manager import NodeManager

class NodeManagerApp:
    def __init__(self):
        self.converter=NodeConverter()
        self.manager=NodeManager()
        self.window=self.load_ui()
        self.window.savedList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # clear selection when focus moves away from savedList
        QApplication.instance().focusChanged.connect(self.on_focus_changed)
        self.bind_events()
        self.refresh_saved()

    def load_ui(self):
        loader=QUiLoader()
        ui_file=QFile("gui/NodeManager.ui")
        ui_file.open(QFile.ReadOnly)
        window=loader.load(ui_file)
        ui_file.close()
        return window

    def bind_events(self):
        self.window.organizeButton.clicked.connect(self.parse_nodes)
        self.window.copyOutputButton.clicked.connect(self.copy_output)
        self.window.saveNodeButton.clicked.connect(self.add_saved)
        self.window.copyLibraryButton.clicked.connect(self.copy_library)
        self.window.deleteNodeButton.clicked.connect(self.delete_node)

        self.window.clearInputButton.clicked.connect(self.clear_input)
        self.window.clearOutputButton.clicked.connect(self.clear_output)

    def parse_nodes(self):
        text=self.window.inputBox.toPlainText()
        nodes=self.converter.convert(text)
        self.manager.set_current(nodes)
        self.show_output()

    def show_output(self):
        text=self.manager.format_nodes(self.manager.get_current())
        self.window.outputBox.setPlainText(text)

    def copy_output(self):
        QApplication.clipboard().setText(
            self.window.outputBox.toPlainText()
        )

    def clear_input(self):
        self.window.inputBox.clear()

    def clear_output(self):
        self.window.outputBox.clear()

    def add_saved(self):
        self.manager.add_to_saved(self.manager.get_current())
        self.refresh_saved()

    def refresh_saved(self):
        scrollbar=self.window.savedList.verticalScrollBar()
        position=scrollbar.value()

        self.window.savedList.clear()

        groups=defaultdict(list)
        country_order=[]

        for node in self.manager.get_saved():
            if node.country_name not in groups:
                country_order.append(node.country_name)

            groups[node.country_name].append(node)

        for country_name in country_order:
            item=QListWidgetItem(country_name)
            item.setData(Qt.UserRole,"country")
            item.setFlags(Qt.NoItemFlags)
            self.window.savedList.addItem(item)

            nodes=groups[country_name]
            nodes.sort(key=lambda x:x.number)

            for node in nodes:
                item = QListWidgetItem(node.output_line("default"))
                # mark as node and store the node object for accurate mapping
                item.setData(Qt.UserRole, "node")
                item.setData(Qt.UserRole + 1, node)
                self.window.savedList.addItem(item)

        QTimer.singleShot(
            0,
            lambda: scrollbar.setValue(position)
        )

    def get_selected_nodes(self):
        selected=self.window.savedList.selectedItems()
        nodes=[]

        for item in selected:
            if item.data(Qt.UserRole)=="country":
                continue

            node = item.data(Qt.UserRole + 1)
            if node:
                nodes.append(node)

        return nodes

    def copy_library(self):
        nodes=self.get_selected_nodes()

        # if nothing selected, copy the entire displayed library in the same order
        if not nodes:
            nodes = []
            for i in range(self.window.savedList.count()):
                item = self.window.savedList.item(i)
                if item.data(Qt.UserRole) == "country":
                    continue
                node = item.data(Qt.UserRole + 1)
                if node:
                    nodes.append(node)

        if not nodes:
            return

        text="\n".join(
            node.output_line("default")
            for node in nodes
        )

        QApplication.clipboard().setText(text)

    def delete_node(self):
        nodes=self.get_selected_nodes()

        if not nodes:
            return

        for node in nodes:
            self.manager.delete(
                node.ip,
                node.port
            )

        self.refresh_saved()

    def on_focus_changed(self, old, new):
        # if focus moved away from savedList (or its children), clear selection
        try:
            if old and (old is self.window.savedList or self.window.savedList.isAncestorOf(old)):
                if not (new and (new is self.window.savedList or self.window.savedList.isAncestorOf(new))):
                    self.window.savedList.clearSelection()
        except Exception:
            # ignore any unexpected errors during focus handling
            pass

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=NodeManagerApp()
    window.window.show()
    sys.exit(app.exec())
