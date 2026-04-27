from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from starlette import status
from schemas.users import UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserRequest, UserChangePasswordRequest
from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])

# 用户注册
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果

    # 验证用户是否存在
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")

    user = await users.create_user(db, user_data)

    # 生成 Token
    token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="用户注册成功", data=response_data)

    # return {
    #     "code": 200,
    #     "message": "用户注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }


# 用户登录
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑： 验证用户书否存在 -> 验证密码 -> 生成 Token -> 响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="用户登录成功", data=response_data)


# 获取个人信息
# 查 Token 查用户 -> 封装 crud -> 功能整合成一个工具函数 -> 路由导入使用
@router.get("/info")
async def get_user_info(user=Depends(get_current_user)):
    return success_response(message="获取个人信息成功", data=UserInfoResponse.model_validate(user))


# 修改个人信息
# 验证 Token -> 更新（用户输入数据，put 提交）
@router.put("/update")
async def update_user_info(
        update_user_data: UserUpdateRequest,
        user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    updated_user = await users.update_user(db, user.username, update_user_data)
    return success_response(message="修改个人信息成功", data=UserInfoResponse.model_validate(updated_user))


# 修改密码
@router.put("/password")
async def update_password(
        change_password: UserChangePasswordRequest,
        user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    change_result = await users.change_password(db, user, change_password.old_password, change_password.new_password)
    if not change_result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="原密码错误，修改失败")

    return success_response(message="修改密码成功")
