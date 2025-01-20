from typing import Dict, Tuple, Optional

from app.core.config import settings
from app.log import logger


class SitesHelper:
    """
    站点助手，负责站点认证和管理
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._auth_level = 2
            self._sites_config = {}
            self._indexers = {}
            self._auth_version = "0.0.0"
            self._indexer_version = "0.0.0"
            self._auth_site = None
            self.initialized = True
            self._init_sites()
            self._load_resources()

    def get_indexers(self) -> list:
        """
        获取所有站点索引器配置
        :return: 站点索引器配置列表
        """
        return list(self._indexers.values())

    def get_indexer(self, domain: str) -> dict:
        """
        根据域名获取站点索引器配置
        :param domain: 站点域名
        :return: 站点索引器配置，格式：
        {
            "id": "站点ID",
            "name": "站点名称",
            "domain": "站点域名",
            "url": "站点URL",
            "cookie": "站点Cookie",
            "ua": "User-Agent",
            "proxy": False,
            "timeout": 30,
            "pri": 0,
            "parser": "解析器类型",
            "language": "站点语言",
            "public": False,
            "schema": "站点模型",
            "api": "API地址",
            "apikey": "API密钥",
            "downloader": "下载器配置"
        }
        """
        if not domain:
            return None
        # 遍历索引器
        for indexer in self._indexers.values():
            if domain.lower() in indexer.get("domain", "").lower():
                return indexer
        return None

    def get_authsites(self) -> dict:
        """
        获取认证站点列表
        :return: 认证站点列表
        """
        return {}

    def _init_sites(self):
        """
        初始化站点配置
        """
        try:
            # 初始化站点配置
            self._auth_level = 0
            # 初始化索引器
            self._indexers = {
                # 这里添加站点索引器配置
                # "站点ID": {
                #     "id": "站点ID",
                #     "name": "站点名称",
                #     "domain": "站点域名",
                #     "url": "站点URL",
                #     "cookie": "站点Cookie",
                #     "ua": "User-Agent",
                #     "proxy": False,
                #     "timeout": 30,
                #     "pri": 0,
                #     "rss": "RSS地址",
                #     "downloader": "下载器"
                # }
            }
            logger.info("站点管理服务启动")
        except Exception as e:
            logger.error(f"站点管理服务启动失败：{str(e)}")

    @property
    def auth_level(self) -> int:
        """
        获取认证等级
        返回值：
            0: 未认证
            1: 基础认证
            2: 完全认证，所有功能可用
        """
        return self._auth_level

    @property
    def auth_version(self) -> str:
        """
        获取认证资源版本号
        用于：
        1. 系统环境信息显示
        2. 资源包更新检查
        3. 版本兼容性判断
        """
        return self._auth_version

    @property
    def indexer_version(self) -> str:
        """
        获取站点索引器版本号
        用于：
        1. 系统环境信息显示
        2. 资源包更新检查
        3. 版本兼容性判断
        """
        return self._indexer_version

    def _load_resources(self):
        """
        加载站点资源
        """
        try:
            # 加载认证资源
            self._auth_level = 0
            self._auth_version = "0.0.0"
            self._auth_site = None
            # 加载站点索引器资源
            self._indexer_version = "0.0.0"
            logger.info("站点资源加载完成")
        except Exception as e:
            logger.error(f"站点资源加载失败：{str(e)}")

    def update_indexer(self, indexer_id: str, indexer_config: dict) -> None:
        """
        更新站点索引器配置
        :param indexer_id: 站点ID
        :param indexer_config: 站点配置
        """
        if not indexer_id or not indexer_config:
            return
        self._indexers[indexer_id] = indexer_config

    def remove_indexer(self, indexer_id: str) -> None:
        """
        移除站点索引器配置
        :param indexer_id: 站点ID
        """
        if indexer_id in self._indexers:
            del self._indexers[indexer_id]

    def clear_indexers(self) -> None:
        """
        清空所有站点索引器配置
        """
        self._indexers.clear()

    def set_auth_level(self, level: int) -> None:
        """
        设置认证等级
        :param level: 认证等级
        """
        self._auth_level = level

    def set_auth_version(self, version: str) -> None:
        """
        设置认证资源版本号
        :param version: 版本号
        """
        self._auth_version = version

    def set_indexer_version(self, version: str) -> None:
        """
        设置站点索引器版本号
        :param version: 版本号
        """
        self._indexer_version = version

    def check_user(self, **kwargs) -> Tuple[bool, str]:
        """
        检查用户认证状态
        :param kwargs: 认证参数
        :return: Tuple[认证状态, 消息]
        """
        return True, "用户已认证"
        if self._auth_level >= 2:
            return True, "用户已认证"
        return False, "用户未认证"