# GUI Agent

基于视觉的 GUI 自动化框架，使用 ReAct Agent 模式控制电脑屏幕。

## 特性

- **纯视觉方案**：跨平台通用，支持任何 GUI 界面
- **ReAct Agent**：自主决策，多轮迭代完成复杂任务
- **Token 优化**：截图历史裁剪，只保留最近 5 张截图
- **归一化坐标**：0-1000 坐标系统，适配不同分辨率

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

```python
from gui_agent import ReActAgent, AgentConfig, get_all_tools
from gui_agent.tools import screenshot

# 配置
config = AgentConfig(
    api_url="https://api.example.com/v1/chat/completions",
    api_key="your-api-key",
    model="gemini-3-flash-preview",
)

# 创建 Agent
agent = ReActAgent(config=config, system_prompt="你是一个 GUI 自动化助手...")

# 注册工具
for tool in get_all_tools():
    agent.register_tool(tool)

# 运行
initial = screenshot()
result = agent.run("打开浏览器", image_base64=initial.image_base64)
```

## 工具集

| 工具 | 说明 |
|------|------|
| `screenshot` | 截取当前屏幕 |
| `click(x, y)` | 点击指定坐标 |
| `double_click(x, y)` | 双击指定坐标 |
| `right_click(x, y)` | 右键点击 |
| `type_text(text)` | 在当前焦点输入文本 |
| `scroll(x, y, direction, amount)` | 滚动屏幕 |

坐标使用 0-1000 归一化坐标系统。

## 目录结构

```
gui-agent/
├── gui_agent/              # 核心包
│   ├── agent/              # Agent 模块
│   ├── tools/              # 工具模块
│   └── config/             # 配置模块
├── examples/               # 示例
├── docs/                   # 文档
└── screenshots/            # 截图存储
```

## 文档

- [技术方案选型](docs/technical_selection.md)
