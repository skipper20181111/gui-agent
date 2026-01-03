"""工具模块"""

from ..agent.base import Tool

from .screenshot import SCREENSHOT_TOOL, screenshot
from .mouse import CLICK_TOOL, click
from .keyboard import TYPE_TEXT_TOOL, type_text
from .scroll import SCROLL_TOOL, scroll


def get_all_tools() -> list[Tool]:
    """获取所有 GUI 工具"""
    return [
        SCREENSHOT_TOOL,
        CLICK_TOOL,
        TYPE_TEXT_TOOL,
        SCROLL_TOOL,
    ]


__all__ = [
    "get_all_tools",
    "screenshot",
    "click",
    "type_text",
    "scroll",
    "SCREENSHOT_TOOL",
    "CLICK_TOOL",
    "TYPE_TEXT_TOOL",
    "SCROLL_TOOL",
]
