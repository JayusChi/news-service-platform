from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 目标： FastAPI、Pydantic、ORM 对象，都要正常响应 -> code message data
    return JSONResponse(jsonable_encoder(content))