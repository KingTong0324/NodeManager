import os
import sys

def get_base_dir():
    """
    返回运行时的基础路径：
    - 打包后（onefile/onedir）优先取 sys._MEIPASS（PyInstaller 在 onefile 时解压到此目录）
    - 未打包则返回项目根目录
    """
    # PyInstaller sets _MEIPASS to the temp folder where it unpacks files
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return base

    # legacy frozen check
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # project root (one level up from this module)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resource_path(*relative_parts):
    """
    返回资源的绝对路径。传入相对路径片段，例如 ('gui','NodeManager.ui')
    """
    return os.path.join(get_base_dir(), *relative_parts)
