from fastapi import APIRouter
from service.service import Service
from ReqModel.main import WebURLRequest, ErrorResponse, SuccessResponse, UserQueryRequest

router = APIRouter(prefix="/api")
service = Service()

@router.post("/load_script/")
def load_web_scripts(urlObj: WebURLRequest):
    res = service.load_web_page_data(urlObj.url)
    if res.get("status"):
        return SuccessResponse(res_message=res.get("message"))
    else:
        return ErrorResponse(res_message=res.get("message"))
               
@router.post("/query/")
def user_query(queryObj: UserQueryRequest):
    res = service.handle_user_query(queryObj)
    if res.get("status"):
        return SuccessResponse(res_message=res.get("data"))
    else:
        return ErrorResponse(res_message=res.get("data"))
    
