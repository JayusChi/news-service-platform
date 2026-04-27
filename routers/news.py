"""
模块化路由，存放各种各样的路由，通过路由来调用 crud 封装好的函数响应结果
接口实现流程
1、模块化路由 -> API 接口规范文档
2、定义模型类 -> 数据库表（数据库设计文档）
3、在 crud 文件夹里面创建文件，封装操作数据库的方法
4、在路由处理函数里面调用 crud 封装好的方法，响应结果
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from crud import news, news_cache
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db

# 创建 APIRouter 实例
# prefix 路由前缀（API 接口规范文档）    tag 分组 标签
router = APIRouter(prefix="/api/news", tags=["news"])


# 获取新闻分类
@router.get("/categories")
async def get_categores(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    categories = await news_cache.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

# 获取新闻列表
@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db),
        category_id : int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
):
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db, category_id, offset, page_size)
    news_count = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < news_count
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": news_count,
            "hasMore": has_more
        }
    }

# 获取新闻详情
@router.get("/details")
async def get_news_details(
        news_id: int = Query(..., alias="newsId"),
        db: AsyncSession = Depends(get_db),
):
    # 获取新闻详情
    news_details = await news_cache.get_news_details(db, news_id)
    if not news_details:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 更新阅读量
    views_res = await news.increase_news_views(db, news_details.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 获取相关推荐
    related_news = await news_cache.get_related_news(db, news_details.id, news_details.category_id)
    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_details.id,
            "title": news_details.title,
            "content": news_details.content,
            "image": news_details.image,
            "author": news_details.author,
            "publishTime": news_details.publish_time,
            "categoryId": news_details.category_id,
            "views": news_details.views,
            "relatedNews": related_news
          }
    }

