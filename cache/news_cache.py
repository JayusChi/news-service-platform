"""
新闻相关的缓存方法：新闻分类的读取和写入
key: value
"""

from typing import List, Dict, Any, Optional
from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"


# 获取 新闻分类 的缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 写入 新闻分类 的缓存：缓存的数据，过期时间
# 分类、配置：7200     列表：600     详情：1800      验证码：120
async def set_cache_categories(data: list[Dict[str, Any]], expire: int=7200):
    return await set_cache(CATEGORIES_KEY, data, expire)


# 获取 新闻列表 的缓存
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)


# 写入 新闻列表 的缓存
# key = news_list: 分类id: 页码: 每页数量
async def set_cache_news_list(category_id: Optional[int], page: int, page_size: int, data: list[dict[str, Any]], expire: int=1800):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await set_cache(key, data, expire)


# 获取 新闻详情 的缓存
async def get_cached_news_detail(news_id: int) -> Optional[Dict[str, Any]]:
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_json_cache(key)


# 写入 新闻详情 的缓存
async def cache_news_detail(news_id: int, news_data: Dict[str, Any], expire: int = 300) -> bool:
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key, news_data, expire)


# 获取 相关新闻 的缓存
async def get_cached_related_news(news_id: int, category_id: int) -> Optional[List[Dict[str, Any]]]:
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await get_json_cache(key)


# 写入 相关新闻 的缓存
async def cache_related_news(news_id: int, category_id: int, related_list: List[Dict[str, Any]],
                             expire: int = 1800) -> bool:
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await set_cache(key, related_list, expire)



