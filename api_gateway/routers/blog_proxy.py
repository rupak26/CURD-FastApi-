from fastapi import APIRouter, Request
from ..utils.forwarder import forward_request

router = APIRouter()

BLOG_SERVICE_URL = "http://localhost:8001"  


@router.api_route("/api/v1/blog/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def blog_proxy(request: Request, full_path: str):
    target_url = f"{BLOG_SERVICE_URL}/api/v1/blog/{full_path}"
    return await forward_request(request, target_url)



# https://github.com/baranbartu/microservices-with-fastapi/blob/master/gateway/auth.py