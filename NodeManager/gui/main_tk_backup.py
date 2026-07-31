import tkinter as tk
from tkinter import filedialog, messagebox

from core.converter import NodeConverter
from core.node_manager import NodeManager



class NodeManagerApp:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "NodeManager"
        )

        self.root.geometry(
            "1200x700"
        )


        self.converter = NodeConverter()

        self.manager = NodeManager()



        self.create_ui()



    # =====================
    # 创建界面
    # =====================

    def create_ui(self):


        main_frame = tk.Frame(
            self.root
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



        # =====================
        # 三列
        # =====================


        left = tk.Frame(
            main_frame
        )

        middle = tk.Frame(
            main_frame
        )

        right = tk.Frame(
            main_frame
        )



        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        middle.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )



        # =====================
        # 输入节点
        # =====================

        tk.Label(
            left,
            text="输入节点"
        ).pack()



        self.input_box = tk.Text(
            left
        )

        self.input_box.pack(
            fill="both",
            expand=True
        )



        tk.Button(
            left,
            text="解析节点",
            command=self.parse_nodes
        ).pack(
            fill="x",
            pady=5
        )



        tk.Button(
            left,
            text="清空",
            command=lambda:
                self.input_box.delete(
                    "1.0",
                    tk.END
                )
        ).pack(
            fill="x"
        )



        # =====================
        # 输出结果
        # =====================


        tk.Label(
            middle,
            text="输出结果"
        ).pack()



        self.output_box = tk.Text(
            middle
        )

        self.output_box.pack(
            fill="both",
            expand=True
        )



        tk.Button(
            middle,
            text="复制结果",
            command=self.copy_output
        ).pack(
            fill="x",
            pady=5
        )



        tk.Button(
            middle,
            text="加入节点库",
            command=self.add_saved
        ).pack(
            fill="x"
        )



        # =====================
        # 已保存节点
        # =====================


        tk.Label(
            right,
            text="已保存节点"
        ).pack()



        self.saved_box = tk.Listbox(
            right
        )

        self.saved_box.pack(
            fill="both",
            expand=True
        )



        tk.Button(
            right,
            text="加载节点文件",
            command=self.load_nodes
        ).pack(
            fill="x",
            pady=5
        )



        tk.Button(
            right,
            text="保存节点文件",
            command=self.save_nodes
        ).pack(
            fill="x"
        )



        tk.Button(
            right,
            text="刷新列表",
            command=self.refresh_saved
        ).pack(
            fill="x"
        )



    # =====================
    # 解析节点
    # =====================
    def parse_nodes(self):

        text = self.input_box.get(
            "1.0",
            tk.END
        )


        nodes = self.converter.convert(
            text
        )


        self.manager.set_current(
            nodes
        )


        self.show_output()



    # =====================
    # 显示输出
    # =====================

    def show_output(self):

        self.output_box.delete(
            "1.0",
            tk.END
        )


        text = self.manager.format_nodes(
            self.manager.get_current()
        )


        self.output_box.insert(
            tk.END,
            text
        )



    # =====================
    # 加入节点库
    # =====================

    def add_saved(self):

        self.manager.add_to_saved(
            self.manager.get_current()
        )


        self.refresh_saved()



    # =====================
    # 刷新保存列表
    # =====================

    def refresh_saved(self):

        self.saved_box.delete(
            0,
            tk.END
        )


        for node in self.manager.get_saved():

            self.saved_box.insert(
                tk.END,
                node.display_name()
            )



    # =====================
    # 保存节点
    # =====================

    def save_nodes(self):

        path = filedialog.asksaveasfilename(

            title="保存节点",

            defaultextension=".json",

            filetypes=[
                (
                    "JSON",
                    "*.json"
                )
            ]
        )


        if not path:

            return



        self.manager.save_file(
            path
        )


        messagebox.showinfo(
            "完成",
            "节点保存成功"
        )



    # =====================
    # 加载节点
    # =====================

    def load_nodes(self):

        path = filedialog.askopenfilename(

            title="加载节点",

            filetypes=[
                (
                    "JSON",
                    "*.json"
                )
            ]
        )


        if not path:

            return



        self.manager.load_file(
            path
        )


        self.refresh_saved()



        messagebox.showinfo(
            "完成",
            "节点加载成功"
        )



    # =====================
    # 复制输出
    # =====================

    def copy_output(self):

        text = self.output_box.get(
            "1.0",
            tk.END
        )


        self.root.clipboard_clear()

        self.root.clipboard_append(
            text
        )



        messagebox.showinfo(
            "完成",
            "已复制"
        )





if __name__ == "__main__":


    root = tk.Tk()


    app = NodeManagerApp(
        root
    )


    root.mainloop()