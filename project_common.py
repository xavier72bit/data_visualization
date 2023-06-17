import os.path

__all__ = ["CURRENT_WORKSPACE", "CURRENT_CONFIG_PATH", "CURRENT_LOG_PATH"]

# -----------------------------------------------------
# 常量定义
# -----------------------------------------------------

# 工作目录
CURRENT_WORKSPACE = os.path.abspath('.')
CURRENT_CONFIG_PATH = os.path.join(CURRENT_WORKSPACE, 'config')
CURRENT_LOG_PATH = os.path.join(CURRENT_WORKSPACE, 'logs')
