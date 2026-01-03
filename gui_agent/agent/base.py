"""
Agent 基础类定义
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: dict
    func: Callable[..., Any]


@dataclass
class ToolResult:
    """工具执行结果"""
    text: str
    image_base64: Optional[str] = None  # PNG base64 编码
    

@dataclass
class AgentConfig:
    """Agent 配置"""
    api_url: str
    api_key: str
    model: str
    max_iterations: int = 10
    timeout: int = 120
