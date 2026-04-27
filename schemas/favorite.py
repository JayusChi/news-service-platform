from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import NewsItemBase

class FavoriteCheckRequest(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")


class FavoruteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


# 规划两个类，一个是新闻模型类，一个是收藏的模型类
class FavoriteNewsItemResonse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


# 收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResonse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

