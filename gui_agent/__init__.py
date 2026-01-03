"""
GUI Agent - 基于视觉的 GUI 自动化框架
"""

from .agent import Tool, ToolResult, AgentConfig, ReActAgent
from .tools import get_all_tools, screenshot, click, type_text, scroll
from .config import SCREENSHOT_DIR, DEFAULT_API_TIMEOUT, DEFAULT_MAX_ITERATIONS

__version__ = "0.1.0"

__all__ = [
    # Agent
    "Tool",
    "ToolResult", 
    "AgentConfig",
    "ReActAgent",
    # Tools
    "get_all_tools",
    "screenshot",
    "click",
    "type_text",
    "scroll",
    # Config
    "SCREENSHOT_DIR",
    "DEFAULT_API_TIMEOUT",
    "DEFAULT_MAX_ITERATIONS",
]
