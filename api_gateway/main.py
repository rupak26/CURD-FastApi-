from fastapi import FastAPI, Request , APIRouter , Depends , HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from utils.jwt_decoder import decode_access_token
import asyncio , os


app = FastAPI(title="API Gateway", docs_url=None, redoc_url=None)

security = HTTPBearer()

# Define the microservices and their OpenAPI URLs
MICROSERVICES = {
    "auth": "http://localhost:8080/openapi.json",
    "blog": "http://localhost:8000/openapi.json",
}

# Map prefix to internal microservice base URLs
SERVICE_MAP = {
    "auth": "http://localhost:8080",
    "blog": "http://localhost:8000"
}




@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_MAP:
        return JSONResponse(status_code=404, content={"detail": "Service not found"})

    headers = dict(request.headers)

    # ✅ Only validate token for "blog" service
    if service == "blog":
        auth_header = headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token missing for blog service")

        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

        headers.update({
            "X-User-Id": str(payload["user_id"]),
            "X-User-Email": payload["email"],
            "X-User-Role": payload["user_role"],
        })

    # ✅ Proxy request
    url = f"{SERVICE_MAP[service]}/{path}"
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=headers,
                params=request.query_params
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items() if k.lower() != "content-encoding"}
            )
        except httpx.RequestError as exc:
            return JSONResponse(status_code=500, content={"detail": f"Gateway error: {str(exc)}"})
# async def proxy(
#     service: str, 
#     path: str, 
#     request: Request,
#     ):
#     if service not in SERVICE_MAP:
#         return JSONResponse(status_code=404, content={"detail": "Service not found"})
    
#     if service == "blog":
#         credentials: HTTPAuthorizationCredentials = Depends(security)
#         token = credentials.credentials
#         payload = decode_access_token(token)
#         headers = {
#             "X-User-Id": str(payload["user_id"]),
#             "X-User-Email": payload["email"],
#             "X-User-Role": payload["user_role"],
#             "Content-Type": request.headers.get("content-type", "application/json"),
#             "Authorization": f"Bearer {token}",  
#         }
#     else:
#         headers = request.headers

#     url = f"{SERVICE_MAP[service]}/{path}"

#     body = await request.body()

#     async with httpx.AsyncClient() as client:
#         try:
#             # Forward the request method, headers, and body
#             method = request.method
#             body = await request.body()
            
#             response = await client.request(
#                 method=method.upper(),
#                 url=url,
#                 content=body,
#                 headers=request.headers,
#                 params=request.query_params
#             )

#             return Response(
#                 content=response.content,
#                 status_code=response.status_code,
#                 headers=response.headers
#             )
#         except httpx.RequestError as exc:
#             return JSONResponse(status_code=500, content={"detail": f"Gateway error: {str(exc)}"})



@app.get("/openapi-merged.json")
async def merged_openapi():
    merged_paths = {}
    merged_components = {"schemas": {}}
    tags = []

    async with httpx.AsyncClient() as client:
        for name, url in MICROSERVICES.items():
            try:
                res = await client.get(url)
                spec = res.json()
                service_tag = {"name": f"{name.title()} Service"}

                # Add tag
                tags.append(service_tag)

                for path, methods in spec["paths"].items():
                    new_path = f"/{name}{path}"  # Prefix path
                    new_methods = {}

                    for method, details in methods.items():
                        details["tags"] = [f"{name.title()} Service"]
                        new_methods[method] = details

                    merged_paths[new_path] = new_methods

                # Merge schemas
                merged_components["schemas"].update(spec.get("components", {}).get("schemas", {}))

            except Exception as e:
                print(f"Error loading OpenAPI from {url}: {e}")
    return JSONResponse({
        "openapi": "3.0.0",
        "info": {
            "title": "API Gateway Docs",
            "version": "1.0.1",
            "description": "Test API Gateway for all microservices.\n\nThis documentation includes grouped endpoints for all services like User, Employee, etc.",
            "termsOfService": "https://yourcompany.com/terms",
            "contact": {
                "name": "ATI Python Team",
                "url": "https://atilimited.net",
                "email": "support@atilimited.net"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        },

        # ✅ Enables Bearer token on all endpoints unless overridden
        "security": [
            {
                "HTTPBearer": []
            }
        ],

        "paths": merged_paths,

        # ✅ Add securitySchemes here
        "components": {
            **merged_components,  # keep your merged schemas
            "securitySchemes": {
                "HTTPBearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },

        "tags": tags,
    })

    # return JSONResponse({
    #     "openapi": "3.0.0",
    #      "info": {
    #     "title": "API Gateway Docs",
    #     "version": "1.0.1",
    #     "description": "Test API Gateway for all microservices.\n\nThis documentation includes grouped endpoints for all services like User, Employee, etc.",
    #     "termsOfService": "https://yourcompany.com/terms",
    #     "contact": {
    #         "name": "ATI Python Team",
    #         "url": "https://atilimited.net",
    #         "email": "support@atilimited.net"
    #     },
    #     "license": {
    #         "name": "Apache 2.0",
    #         "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    #     }
    # },
    #     "paths": merged_paths,
    #     "components": merged_components,
    #     "tags": tags,
    # })


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Gateway Swagger UI</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css">
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script>
          SwaggerUIBundle({
            url: '/openapi-merged.json',
            dom_id: '#swagger-ui'
          });
        </script>
      </body>
    </html>
    """)

