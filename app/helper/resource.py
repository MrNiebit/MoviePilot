import json
from pathlib import Path

from app.core.config import settings
from app.helper.sites import SitesHelper
from app.log import logger
from app.utils.http import RequestUtils
from app.utils.singleton import Singleton
from app.utils.string import StringUtils
from app.utils.system import SystemUtils


class ResourceHelper(metaclass=Singleton):
    """
    检测和更新资源包
    """
    # 资源包的git仓库地址
    _repo = f"{settings.GITHUB_PROXY}https://raw.githubusercontent.com/jxxghp/MoviePilot-Resources/main/package.json"
    _files_api = f"https://api.github.com/repos/jxxghp/MoviePilot-Resources/contents/resources"
    _base_dir: Path = settings.ROOT_PATH

    def __init__(self):
        self.siteshelper = SitesHelper()
        self.check()

    @property
    def proxies(self):
        return None if settings.GITHUB_PROXY else settings.PROXY

    def check(self):
        """
        检测是否有更新，如有则下载安装
        """
        if not settings.AUTO_UPDATE_RESOURCE:
            return
        if SystemUtils.is_frozen():
            return
        logger.info("开始检测资源包版本...")
        res = RequestUtils(proxies=self.proxies, headers=settings.GITHUB_HEADERS, timeout=10).get_res(self._repo)
        if res:
            try:
                resource_info = json.loads(res.text)
            except json.JSONDecodeError:
                logger.error("资源包仓库数据解析失败！")
                return
        else:
            logger.warn("无法连接资源包仓库！")
            return
        online_version = resource_info.get("version")
        if online_version:
            logger.info(f"最新资源包版本：v{online_version}")
        # 需要更新的资源包
        need_updates = {}
        # 资源明细
        resources: dict = resource_info.get("resources") or {}
        for rname, resource in resources.items():
            rtype = resource.get("type")
            platform = resource.get("platform")
            target = resource.get("target")
            version = resource.get("version")
            # 判断平台
            if platform and platform != SystemUtils.platform():
                continue
            # 判断版本号
            if rtype == "auth":
                # 站点认证资源
                local_version = self.siteshelper.auth_version
            elif rtype == "sites":
                # 站点索引资源
                local_version = self.siteshelper.indexer_version
            else:
                continue
            if StringUtils.compare_version(version, ">", local_version):
                logger.info(f"{rname} 资源包有更新，最新版本：v{version}")
            else:
                continue
            # 需要安装
            need_updates[rname] = target
        if need_updates:
            logger.info("发现可用的资源包更新，但已禁用自动下载功能")
            for rname in need_updates.keys():
                logger.info(f"资源包 {rname} 有可用更新，请手动更新")
        else:
            logger.info("所有资源已最新，无需更新")
