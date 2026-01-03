"""全局配置"""

from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 截图保存目录
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"

# API 默认配置
DEFAULT_API_TIMEOUT = 120
DEFAULT_MAX_ITERATIONS = 20

# 截图延迟（毫秒）
DEFAULT_SCREENSHOT_DELAY_MS = 500

# 最大保留截图数量（用于 Token 优化）
MAX_SCREENSHOTS_IN_HISTORY = 5
