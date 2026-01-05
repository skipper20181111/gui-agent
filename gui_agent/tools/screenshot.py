"""截图工具"""

from ..agent.base import Tool, ToolResult
from .base import screen_capture


def screenshot() -> ToolResult:
    """截取当前屏幕"""
    image_b64 = screen_capture.capture(delay_ms=0)
    return ToolResult(
        text="已截取当前屏幕截图。",
        image_base64=image_b64
    )


SCREENSHOT_TOOL = Tool(
    name="screenshot",
    description="截取当前屏幕截图",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    },
    func=screenshot
)
