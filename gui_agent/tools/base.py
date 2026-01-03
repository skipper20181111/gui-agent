"""
工具基础类 - 屏幕截图
"""

import base64
import platform
import subprocess
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pyautogui
from PIL import Image

from ..config import SCREENSHOT_DIR


class ScreenCapture:
    """屏幕截图类，封装截图逻辑"""
    
    def __init__(self):
        self.scale_factor = self._get_scale_factor()
    
    def _get_scale_factor(self) -> float:
        """获取屏幕缩放因子（macOS Retina）"""
        if platform.system() != "Darwin":
            return 1.0
        try:
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True,
                text=True
            )
            if "Retina" in result.stdout:
                return 2.0
        except Exception:
            pass
        return 1.0
    
    def capture(self, delay_ms: int = 0) -> str:
        """
        截取屏幕并返回 base64 编码，同时保存到本地
        
        Args:
            delay_ms: 截图前等待的毫秒数，0 表示不等待
            
        Returns:
            PNG 图片的 base64 编码字符串
        """
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        
        screenshot = pyautogui.screenshot()
        
        # Retina 屏幕缩放
        if self.scale_factor > 1:
            new_size = (
                int(screenshot.width / self.scale_factor),
                int(screenshot.height / self.scale_factor)
            )
            screenshot = screenshot.resize(new_size, Image.LANCZOS)
        
        # 保存截图到本地
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        screenshot.save(SCREENSHOT_DIR / filename, format="PNG")
        
        # 转换为 PNG base64
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


# 全局截图实例
screen_capture = ScreenCapture()
