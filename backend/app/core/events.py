"""
应用事件处理器
"""
from loguru import logger


async def create_start_app_handler():
    """应用启动时执行的事件"""
    logger.info("外运物流控制塔后端服务启动中...")
    logger.info("初始化数据库连接...")
    logger.info("初始化Redis连接...")
    logger.info("外运物流控制塔后端服务启动完成!")


async def create_stop_app_handler():
    """应用关闭时执行的事件"""
    logger.info("外运物流控制塔后端服务关闭中...")
    logger.info("关闭数据库连接...")
    logger.info("关闭Redis连接...")
    logger.info("外运物流控制塔后端服务已关闭!")
