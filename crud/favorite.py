from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News


# 检查收藏状态（用户是否收藏了某一条新闻）
async def is_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    query = select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    result = await db.execute(query)
    # 是否有收藏记录：返回的是布尔值  返回 True代表收藏了   False代表没收藏
    return result.scalar_one_or_none() is not None


# 添加收藏
async def add_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    favorite = Favorite(news_id=news_id, user_id=user_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 取消收藏
async def delete_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    stmt = delete(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    res = await db.execute(stmt)
    await db.commit()
    return res.rowcount > 0


# 获取收藏列表
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 100
):
    # 收藏的新闻总量
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # 获取收藏列表 - 联表查询 join() + 收藏时间排序 + 分页
    offset = (page - 1) * page_size
    query = ((select(News, Favorite.created_at.label("faverite_time"), Favorite.id.label("faverite_id"))
     .join(Favorite, Favorite.news_id == News.id)
     .where(Favorite.user_id == user_id)
     .order_by(Favorite.created_at.desc())
     .offset(offset).limit(page_size))
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 清空收藏列表
async def remove_all_favorite(
        db: AsyncSession,
        user_id: int
):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()

    # 返回删除的数量
    return result.rowcount or 0
