import config
import os
from fastapi import FastAPI
from controller.main import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ReqModel.main import ErrorResponse

app = FastAPI()
app.include_router(router)

origins = [ 
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^chrome-extension://.*$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def verify_extension_id(request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    expected_id = os.getenv("BACKEND_EXTENSION_AUTH_ID")
    received_id = request.headers.get("X-EXTENSION-AUTH-ID")
    if received_id != expected_id:
        print("Invalid AUTH ID received:", received_id)
        return JSONResponse(content=ErrorResponse(res_message="Invalid AUTH ID.").dict(), status_code=401)
    response = await call_next(request)
    return response