"""工具模块"""

from ..agent.base import Tool

from .screenshot import SCREENSHOT_TOOL, screenshot
from .mouse import CLICK_TOOL, click
from .keyboard import TYPE_TEXT_TOOL, type_text
from .scroll import SCROLL_TOOL, scroll
from .sandbox import PYTHON_TOOL, execute_python


def get_all_tools() -> list[Tool]:
    """获取所有 GUI 工具"""
    return [
        SCREENSHOT_TOOL,
        CLICK_TOOL,
        TYPE_TEXT_TOOL,
        SCROLL_TOOL,
    ]


def get_sandbox_tools() -> list[Tool]:
    """获取沙箱工具"""
    return [PYTHON_TOOL]


__all__ = [
    "get_all_tools",
    "get_sandbox_tools",
    "screenshot",
    "click",
    "type_text",
    "scroll",
    "execute_python",
    "SCREENSHOT_TOOL",
    "CLICK_TOOL",
    "TYPE_TEXT_TOOL",
    "SCROLL_TOOL",
    "PYTHON_TOOL",
]
