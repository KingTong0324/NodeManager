# NodeManager for Cloudflare优选ip

### 节点整理器（仅支持IPV4）
注：本项目为测试项目，代码均由AI生成。

<img width="1251" height="762" alt="image" src="https://github.com/user-attachments/assets/c60e9bc3-5537-4bb4-86c4-e397db66d2ec" />

## 项目概览

**NodeManager** 是一个功能完整的 Python 桌面应用，主要用于**解析、整理和管理网络节点信息**。

### 核心功能
- 📝 **解析节点文本** - 从输入文本中自动提取 IP、端口、地理位置、速度、延迟等信息
- 💾 **保存节点库** - 将节点信息持久化保存到本地数据库
- 🎯 **格式化输出** - 按指定格式输出节点信息
- 📊 **分组管理** - 按国家分组展示和管理节点，IP自动排序，自动编号
- ✂️ **便捷操作** - 支持复制、删除、清空等常用操作

## 架构设计

```
parser → Node → converter → manager → GUI
```

### 分层结构

#### 1. **`parser/` 解析层** - 提取不同类型的信息
- `ip_parser.py` - 解析 IP 和端口
- `location_parser.py` - 解析地理位置和机场代码
- `latency_parser.py` - 解析延迟信息
- `speed_parser.py` - 解析速度信息

#### 2. **`core/` 核心业务层**
- `node_model.py` - 节点数据模型，定义节点属性和序列化方法
- `converter.py` - 文本转换为 Node 对象，处理国家默认机场补全
- `node_manager.py` - 节点管理逻辑，处理当前节点和保存节点
- `storage.py` - 数据持久化操作
- `node_database.py` - 数据库操作和节点查询

#### 3. **`gui/` 用户界面层**
- `NodeManager.ui` - Qt Designer 设计文件（PySide6）
- `delegate.py` - 自定义列表项渲染器
- `main.py` - 应用主程序入口

### 主要模块功能

| 模块 | 功能描述 |
|------|--------|
| **Node** | 节点数据模型，存储 IP、港口、国家、城市、机场代码、速度、延迟等属性 |
| **NodeConverter** | 文本行转换为 Node 对象，自动补全国家默认机场代码 |
| **NodeManager** | 管理当前节点和已保存节点，处理增删改查操作 |
| **NodeDatabase** | 节点数据库，支持添加、删除、查询节点 |
| **GUI** | PySide6 Qt 界面，提供可视化的节点管理界面 |

## UI 交互特性

### 快捷键
- **Ctrl+C** - 复制选中的节点
- **Delete** - 删除选中的节点
- **Ctrl+A** - 全选
- **Ctrl+Z** - 撤销
- **Ctrl+X** - 剪切
- **Ctrl+V** - 粘贴

### 用户体验
- 🌍 中文菜单 - 所有菜单文本本地化，支持中文
- 🎯 焦点管理 - 智能管理焦点状态，避免误操作
- 📋 批量操作 - 支持多选节点进行批量复制、删除

## 项目配置规则

见 `AI_RULES.md` 中的开发规则：

### 禁止事项
- ❌ 禁止大规模重构
- ❌ 禁止修改项目目录结构
- ❌ 禁止更换技术方案
- ❌ 禁止替换已有架构

### 修改原则
- 修改前说明原因和影响范围
- 一次修改最多涉及 1-3 个文件
- 禁止修改已有类名、函数名、变量名（除非明确要求）
- 禁止修改 Qt Designer 生成的 objectName
- 禁止删除已有控件
- 禁止改变 UI 文件结构

## 快速开始

### 依赖
- Python 3.7+
- PySide6（Qt for Python）

### 安装依赖
```bash
pip install PySide6
```

### 运行应用
```bash
python main.py
```

## 项目结构
```
NodeManager/
├── main.py                 # 应用主入口
├── README.md              # 项目说明文档
├── AI_RULES.md            # AI 开发规则
├── config/                # 配置文件目录
│   ├── city.json          # 城市映射配置
│   └── format.json        # 输出格式配置
├── core/                  # 核心业务逻辑
│   ├── __init__.py
│   ├── node_model.py      # 节点数据模型
│   ├── converter.py       # 文本转换器
│   ├── node_manager.py    # 节点管理器
│   ├── storage.py         # 数据存储
│   ├── node_database.py   # 数据库操作
│   └── path_utils.py      # 路径工具
├── parser/                # 解析器模块
│   ├── __init__.py
│   ├── ip_parser.py       # IP 解析
│   ├── location_parser.py # 地理位置解析
│   ├── latency_parser.py  # 延迟解析
│   └── speed_parser.py    # 速度解析
├── gui/                   # GUI 界面
│   ├── NodeManager.ui     # Qt 界面文件
│   ├── delegate.py        # 自定义渲染器
│   └── main_tk_backup.py  # Tkinter 备份版本
├── nodes/                 # 节点数据目录
├── output/                # 输出目录
└── config/                # 配置目录
```

## 许可证
项目暂未指定许可证

---

**创建日期**: 2026-08-01  
**语言**: Python 100%
