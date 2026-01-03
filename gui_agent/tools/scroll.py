"""滚动工具 - scroll"""

import pyautogui

from ..agent.base import Tool, ToolResult
from .base import screen_capture


def _normalize_to_screen(x: int, y: int) -> tuple[int, int]:
    """将归一化坐标 (0-1000) 转换为实际屏幕像素坐标"""
    screen_width, screen_height = pyautogui.size()
    actual_x = int(x / 1000 * screen_width)
    actual_y = int(y / 1000 * screen_height)
    return actual_x, actual_y


def scroll(x: int, y: int, direction: str, amount: int = 3) -> ToolResult:
    """
    在指定位置滚动屏幕
    
    Args:
        x: 归一化 X 坐标 (0-1000)
        y: 归一化 Y 坐标 (0-1000)
        direction: 方向 "up" 或 "down"
        amount: 滚动量
    """
    # 先移动鼠标到指定位置
    actual_x, actual_y = _normalize_to_screen(x, y)
    pyautogui.moveTo(actual_x, actual_y)
    
    # 滚动
    scroll_amount = amount if direction == "up" else -amount
    pyautogui.scroll(scroll_amount)
    
    image_b64 = screen_capture.capture(delay_ms=500)
    return ToolResult(
        text=f"已在坐标 ({x}, {y}) 向 {direction} 滚动 {amount} 单位",
        image_base64=image_b64
    )


SCROLL_TOOL = Tool(
    name="scroll",
    description="""在指定位置滚动屏幕。

坐标系统：使用 0-1000 归一化坐标，(0,0) 为左上角，(1000,1000) 为右下角，(500,500) 为屏幕中心。

重要说明：
- amount 是滚轮单位（wheel units），不是像素或屏幕百分比
- 由于操作系统和应用程序的差异，无法精确对应屏幕滚动比例
- 建议值：amount=3 小幅滚动，amount=5 中等滚动，amount=10 大幅滚动
- 如果滚动不够或滚动过多，请查看截图后再次调用调整

使用建议：先用较小的 amount 尝试，根据截图反馈决定是否需要继续滚动。""",
    parameters={
        "type": "object",
        "properties": {
            "x": {
                "type": "integer", 
                "description": "归一化 X 坐标 (0-1000)，指定滚动时鼠标所在位置"
            },
            "y": {
                "type": "integer", 
                "description": "归一化 Y 坐标 (0-1000)，指定滚动时鼠标所在位置"
            },
            "direction": {
                "type": "string",
                "description": "滚动方向：up 向上滚动（查看上方内容），down 向下滚动（查看下方内容）",
                "enum": ["up", "down"]
            },
            "amount": {
                "type": "integer",
                "description": "滚轮单位数量，建议值：3=小幅，5=中等，10=大幅。默认为 3",
                "default": 3
            }
        },
        "required": ["x", "y", "direction"]
    },
    func=scroll
)
