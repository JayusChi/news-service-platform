"""
操作数据库的方法（增删查改）
"""

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

# 获取所有的新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 获取指定分类的新闻列表
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 获取指定分类的新闻总数
async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()    # 只能有一个结果 否则报错


# 获取指定新闻 id的新闻详情
async def get_news_details(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 更新指定新闻 id的新闻阅读量
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的命中了数据 -> 命中了返回 True
    return result.rowcount > 0


# 获取相关推荐新闻
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 3):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.publish_time.desc(),
        News.views.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()

    # 使用列表推导式，筛选返回的信息
    related_news = result.scalars().all()
    return [{
        "id": news_details.id,
        "title": news_details.title,
        "content": news_details.content,
        "image": news_details.image,
        "author": news_details.author,
        "publishTime": news_details.publish_time,
        "categoryId": news_details.category_id,
        "views": news_details.views,
    } for news_details in related_news]