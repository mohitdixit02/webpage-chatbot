from fastapi import APIRouter
from service.service import Service
from reqModel.main import WebURLRequest, ErrorResponse, SuccessResponse, UserQueryRequest, APIResponse

router = APIRouter(prefix="/api")
service = Service()

@router.post("/load_script/")
def load_web_scripts(urlObj: WebURLRequest):
    res = service.load_web_page_data(urlObj.url)
    if res.get("status"):
        return APIResponse(
            res_instance=SuccessResponse(res_message=res.get("message")),
            status_code=200
        )
    else:
        return APIResponse(
            res_instance=ErrorResponse(res_message=res.get("message")),
            status_code=500
        )
               
@router.post("/query/")
def user_query(queryObj: UserQueryRequest):
    res = service.handle_user_query(queryObj)
    if res.get("status"):
        return APIResponse(
            res_instance=SuccessResponse(res_message=res.get("data")),
            status_code=200
        )
    else:
        return APIResponse(
            res_instance=ErrorResponse(res_message=res.get("data")),
            status_code=500
        )
    
