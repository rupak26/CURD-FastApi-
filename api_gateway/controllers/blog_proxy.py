from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.token import decode_access_token
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/api-gateway/blog",
    tags=["Blog Proxy"],
)
security = HTTPBearer()


async def proxy_request(
    request: Request,
    method: str, 
    path: str,
    credentials: HTTPAuthorizationCredentials,
):

    token = credentials.credentials

    # Decode JWT
    payload = decode_access_token(token)

    # Build headers with user data
    headers = {
        "X-User-Id": str(payload["user_id"]),
        "X-User-Email": payload["email"],
        "X-User-Role": payload["user_role"],
        "Content-Type": request.headers.get("content-type", "application/json"),
    }
    body = await request.body()
    target_url = f"http://localhost:8000/api/v1/blog/{path}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method.upper(),
                url=target_url,
                headers=headers,
                content=body
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Blog service error: {exc}")

    return JSONResponse(status_code=response.status_code, content=response.json())




@router.get("/{path:path}")
async def proxy_get(path: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await proxy_request(request, "GET", path, credentials)

@router.post("/{path:path}")
async def proxy_post(path: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await proxy_request(request, "POST", path, credentials)

@router.put("/{path:path}")
async def proxy_put(path: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await proxy_request(request, "PUT", path, credentials)

@router.patch("/{path:path}")
async def proxy_patch(path: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await proxy_request(request, "PATCH", path, credentials)

@router.delete("/{path:path}")
async def proxy_delete(path: str, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await proxy_request(request, "DELETE", path, credentials)
