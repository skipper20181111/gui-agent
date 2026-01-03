"""鼠标工具 - click"""

import pyautogui

from ..agent.base import Tool, ToolResult
from .base import screen_capture


def _normalize_to_screen(x: int, y: int) -> tuple[int, int]:
    """将归一化坐标 (0-1000) 转换为实际屏幕像素坐标"""
    screen_width, screen_height = pyautogui.size()
    actual_x = int(x / 1000 * screen_width)
    actual_y = int(y / 1000 * screen_height)
    return actual_x, actual_y


def click(x: int, y: int, click_type: str = "left") -> ToolResult:
    """
    点击指定坐标
    
    Args:
        x: 归一化 X 坐标 (0-1000)
        y: 归一化 Y 坐标 (0-1000)
        click_type: 点击类型 - left(左键单击), right(右键单击), double(左键双击)
    """
    actual_x, actual_y = _normalize_to_screen(x, y)
    
    if click_type == "double":
        pyautogui.doubleClick(actual_x, actual_y)
        action = "双击"
    elif click_type == "right":
        pyautogui.rightClick(actual_x, actual_y)
        action = "右键点击"
    else:
        pyautogui.click(actual_x, actual_y)
        action = "点击"
    
    image_b64 = screen_capture.capture(delay_ms=500)
    return ToolResult(
        text=f"已{action}坐标 ({x}, {y})",
        image_base64=image_b64
    )


CLICK_TOOL = Tool(
    name="click",
    description="""在指定坐标执行鼠标点击操作。

坐标系统说明：
- 使用 0-1000 归一化坐标，与实际屏幕分辨率无关
- 原点 (0, 0) 在屏幕左上角
- 右下角是 (1000, 1000)
- 例如：屏幕中心坐标为 (500, 500)

点击类型：
- left：左键单击（默认）
- right：右键单击，用于打开右键菜单
- double：左键双击，用于打开文件或选中文字""",
    parameters={
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "X 坐标 (0-1000)，0 是最左边，1000 是最右边"},
            "y": {"type": "integer", "description": "Y 坐标 (0-1000)，0 是最上边，1000 是最下边"},
            "click_type": {
                "type": "string",
                "description": "点击类型：left(左键单击), right(右键单击), double(左键双击)",
                "enum": ["left", "right", "double"],
                "default": "left"
            }
        },
        "required": ["x", "y"]
    },
    func=click
)
