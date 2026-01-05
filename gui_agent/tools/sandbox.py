"""Python 代码执行沙箱工具"""

import subprocess
import sys
import tempfile
from pathlib import Path

from ..agent.base import Tool, ToolResult


def execute_python(code: str, timeout: int = 30) -> ToolResult:
    """
    执行 Python 代码并返回结果
    
    原理：
    1. 将代码写入临时 .py 文件
    2. subprocess 启动新 Python 进程执行
    3. 捕获 stdout/stderr 返回
    4. 超时自动终止
    
    Args:
        code: 要执行的 Python 代码
        timeout: 超时时间（秒），默认 30 秒
        
    Returns:
        ToolResult 包含执行输出或错误信息
    """
    if not code or not code.strip():
        return ToolResult(text="错误：代码不能为空")
    
    try:
        # 创建临时文件写入代码
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            # 执行代码
            result = subprocess.run(
                [sys.executable, str(temp_path)],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # 组合输出
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += f"[stderr]\n{result.stderr}"
            
            if not output:
                output = "(无输出)"
                
            # 添加返回码信息（非零表示异常）
            if result.returncode != 0:
                output += f"\n[退出码: {result.returncode}]"
                
            return ToolResult(text=output)
            
        finally:
            # 清理临时文件
            temp_path.unlink(missing_ok=True)
            
    except subprocess.TimeoutExpired:
        return ToolResult(text=f"执行超时（{timeout}秒），已终止")
    except Exception as e:
        return ToolResult(text=f"执行失败：{type(e).__name__}: {e}")


PYTHON_TOOL = Tool(
    name="execute_python",
    description="执行 Python 代码并返回输出结果。用于数据处理、计算、分析等任务。代码在独立进程中执行，有 30 秒超时限制。",
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "要执行的 Python 代码"
            },
            "timeout": {
                "type": "integer",
                "description": "超时时间（秒），默认 30 秒，最大 120 秒"
            }
        },
        "required": ["code"]
    },
    func=execute_python
)
