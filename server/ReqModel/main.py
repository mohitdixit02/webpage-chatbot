from pydantic import BaseModel, Field
from typing import Annotated, Literal, Union, Dict, Any

# Missing Error Response HttpObject

class WebURLRequest(BaseModel):
    url: str
    
class UserQueryRequest(BaseModel):
    query: str
    externalSearch: Annotated[bool, Field(default=False)]
    behaviour: Annotated[Literal['Explain', 'Summary', 'One-Line'], Field(default="Sumamry")]
    url: str
    
class ErrorResponse(BaseModel):
    res_code: Annotated[int, Field(gt=0, default=500)]
    res_status: Annotated[Literal['error'], Field(default='error')]
    res_message: Annotated[str, Field(default="An unexpected error occurred.")]
    
class SuccessResponse(BaseModel):
    res_code: Annotated[int, Field(gt=0, default=200)]
    res_status: Annotated[Literal['success'], Field(default='success')]
    res_message: Union[str, Dict[str, Any]] = Field(..., description="Response message, can be a string or structured data")