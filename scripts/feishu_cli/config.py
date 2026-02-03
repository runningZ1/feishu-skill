"""
飞书 CLI - 配置管理模块
"""

import json
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


DEFAULT_CONFIG_PATH = Path.home() / ".feishu_config.json"
ENV_PATH = Path(__file__).parent.parent.parent / ".env"


class Config:
    """配置管理类"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self._config = {}
        self._load_env()
        self._load_config()

    def _load_env(self):
        """加载 .env 文件"""
        if HAS_DOTENV and ENV_PATH.exists():
            load_dotenv(ENV_PATH)

    def _load_config(self):
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  配置文件读取失败: {e}")
                self._config = {}
        else:
            self._config = {}

    def save(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已保存到: {self.config_path}")
        except IOError as e:
            print(f"❌ 配置保存失败: {e}")

    def get(self, key: str, default=None):
        """获取配置项"""
        # 优先从环境变量读取
        env_key = f"FEISHU_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value:
            return env_value

        # 其次从配置文件读取
        return self._config.get(key, default)

    def set(self, key: str, value: str):
        """设置配置项"""
        self._config[key] = value

    @property
    def app_id(self) -> Optional[str]:
        """获取应用 ID"""
        return self.get("app_id")

    @property
    def app_secret(self) -> Optional[str]:
        """获取应用密钥"""
        return self.get("app_secret")

    @property
    def default_folder_token(self) -> Optional[str]:
        """获取默认文件夹 token"""
        return self.get("default_folder_token")

    def validate_credentials(self) -> bool:
        """验证凭据是否完整"""
        if not self.app_id:
            print("❌ 未配置 app_id")
            print("   方式1: 在项目根目录创建 .env 文件，添加 FEISHU_APP_ID=xxx")
            print("   方式2: 运行 feishu config set app_id <your_app_id>")
            return False
        if not self.app_secret:
            print("❌ 未配置 app_secret")
            print("   方式1: 在项目根目录创建 .env 文件，添加 FEISHU_APP_SECRET=xxx")
            print("   方式2: 运行 feishu config set app_secret <your_app_secret>")
            return False
        return True


def get_config() -> Config:
    """获取全局配置实例"""
    return Config()
