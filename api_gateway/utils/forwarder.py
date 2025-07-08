import httpx
from fastapi import Request, Response

async def forward_request(request: Request, target_url: str) -> Response:
    method = request.method.lower()
    print("============================================================")
    print(method, target_url)
    print("============================================================")
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await getattr(client, method)(
            url=target_url,
            content=body,
            headers=headers,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
