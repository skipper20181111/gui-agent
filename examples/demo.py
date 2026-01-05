"""
Demo: 使用 ReAct Agent 控制 GUI
"""

from gui_agent import ReActAgent, AgentConfig, get_all_tools
from gui_agent.tools import screenshot, get_sandbox_tools


SYSTEM_PROMPT = """你是一个 GUI 自动化助手，可以通过工具控制电脑屏幕。


## 操作系统
当前是 macOS 系统。

## 打开应用的方法
通过截图找到可能是程序坞的地方，然后找到对应的应用

## 重要规则
1. 每次操作后都会返回屏幕截图，请根据截图判断下一步操作
2. 如果操作失败，尝试其他方法
3. 完成任务后，明确告诉用户已完成
4. 你必须通过工具调用来执行操作，不要只是描述步骤
"""


def main(api_url: str, api_key: str, model: str):
    config = AgentConfig(
        api_url=api_url,
        api_key=api_key,
        model=model,
        max_iterations=10,
        timeout=120
    )
    
    print("=" * 60)
    print("ReAct GUI Agent Demo")
    print("=" * 60)
    
    # 创建 Agent
    agent = ReActAgent(config=config, system_prompt=SYSTEM_PROMPT)
    
    # 注册所有 GUI 工具
    for tool in get_all_tools():
        agent.register_tool(tool)
    
    # 注册沙箱工具（Python 代码执行）
    for tool in get_sandbox_tools():
        agent.register_tool(tool)
    
    # 先截取当前屏幕
    print("\n[Demo] 截取当前屏幕作为初始状态...")
    initial_screenshot = screenshot()
    
    # 运行任务
    task = "请打开 chrome 浏览器，并通过 google 搜索一下委内瑞拉的新闻，必须用scroll看完一整页的新闻标题再做总结"
    task = "请用python计算一下1+1=？并告诉我当前页面是什么？"
    print(f"\n[Demo] 任务: {task}")
    
    result = agent.run(task, image_base64=initial_screenshot.image_base64)
    
    print("\n" + "=" * 60)
    print("任务完成")
    print("=" * 60)
    print(f"最终回复: {result}")


if __name__ == "__main__":
    # 在这里配置你的 API
    API_URL = "https://api.bltcy.ai/v1/chat/completions"
    API_KEY = "sk-F86v2p0Cy0DrDX0igR7ojNxQ2"
    # 请联系作者获取apikey
    MODEL = "gemini-3-flash-preview"

    main(API_URL, API_KEY, MODEL)
