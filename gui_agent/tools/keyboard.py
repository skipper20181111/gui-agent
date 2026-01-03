"""键盘工具 - type_text"""

import platform
import time
from typing import Optional

import pyautogui
import pyperclip

from ..agent.base import Tool, ToolResult
from .base import screen_capture


def _normalize_to_screen(x: int, y: int) -> tuple[int, int]:
    """将归一化坐标 (0-1000) 转换为实际屏幕像素坐标"""
    screen_width, screen_height = pyautogui.size()
    actual_x = int(x / 1000 * screen_width)
    actual_y = int(y / 1000 * screen_height)
    return actual_x, actual_y


def type_text(
    text: str,
    x: Optional[int] = None,
    y: Optional[int] = None,
    press_enter: bool = False
) -> ToolResult:
    """
    输入文本（使用剪贴板方式，支持中文）
    
    Args:
        text: 要输入的文本
        x: 可选，输入前先点击的 X 坐标 (0-1000)
        y: 可选，输入前先点击的 Y 坐标 (0-1000)
        press_enter: 可选，输入完成后是否按回车键
    """
    result_parts = []
    
    # 如果提供了坐标，先点击获取焦点
    if x is not None and y is not None:
        actual_x, actual_y = _normalize_to_screen(x, y)
        pyautogui.click(actual_x, actual_y)
        time.sleep(0.2)
        result_parts.append(f"已点击坐标 ({x}, {y}) 获取焦点")
    
    # 使用剪贴板输入文本
    original = pyperclip.paste()
    pyperclip.copy(text)
    
    # macOS: Command+V, 其他: Ctrl+V
    if platform.system() == "Darwin":
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")
    
    time.sleep(0.3)
    pyperclip.copy(original)  # 恢复剪贴板
    result_parts.append(f"已输入文本: {text}")
    
    # 如果需要按回车
    if press_enter:
        pyautogui.press("enter")
        result_parts.append("已按回车键")
    
    image_b64 = screen_capture.capture(delay_ms=500)
    return ToolResult(
        text="，".join(result_parts),
        image_base64=image_b64
    )


TYPE_TEXT_TOOL = Tool(
    name="type_text",
    description="""输入文本（支持中文）。

使用方式：
1. 仅输入文本：type_text(text="hello") - 在当前焦点位置输入
2. 点击后输入：type_text(text="hello", x=?, y=?) - 先点击坐标获取焦点，再输入
3. 输入后回车：type_text(text="hello", press_enter=true) - 输入后按回车键提交
4. 完整流程：type_text(text="hello", x=?, y=?, press_enter=true) - 点击获取焦点 → 输入文本 → 按回车提交

典型场景：
- 搜索框：提供坐标点击搜索框，输入关键词，press_enter=true 提交搜索
- 表单填写：提供坐标点击输入框，输入内容，不按回车继续填写下一项""",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "要输入的文本"},
            "x": {"type": "integer", "description": "可选，输入前先点击的 X 坐标 (0-1000)"},
            "y": {"type": "integer", "description": "可选，输入前先点击的 Y 坐标 (0-1000)"},
            "press_enter": {"type": "boolean", "description": "可选，输入完成后是否按回车键", "default": False}
        },
        "required": ["text"]
    },
    func=type_text
)
