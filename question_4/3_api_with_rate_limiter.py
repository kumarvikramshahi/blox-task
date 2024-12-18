# To implement rate limiting, we can store the client's IP address, the number of requests they have made in the last 60 seconds, and the epoch time of their last request. To manage this data efficiently, we can use Redis as a caching solution. The rate limit check function can be implemented as middleware that verifies the request rate before allowing access to the main content.

# Below is API implementation(for time being i'm only using variables to store cache data)......
# below middleware will execute before every endpoint

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

REQUEST_LIMIT_PER_MIN = 15
RATE_LIMIT_PENALTY = 60  # sec
RATE_LIMIT_WAIT_TIME = 60  # sec

localStore = {
    "ip-address": {
        "count": 20,
        "last_request_time": 12334,  # epoch time in millisecond
    }
}


@app.middleware("http")
async def RateLimiter(request: Request, call_next):
    clientIp = request.client.host

    lastRequestTime = localStore.get(clientIp, {}).get("last_request_time", 0)
    lastRequestTime = lastRequestTime / 1000  # millisecond to second
    reqCount = localStore.get(clientIp, {}).get("count", 0)
    currentTime = datetime.now().timestamp()
    # check if req within 60 sec
    if currentTime - lastRequestTime <= RATE_LIMIT_WAIT_TIME:
        reqCount += 1
        localStore[clientIp] = {
            "count": reqCount,
            "last_request_time": currentTime * 1000,
        }
        if reqCount > REQUEST_LIMIT_PER_MIN:
            localStore[clientIp]["last_request_time"] = (
                lastRequestTime + RATE_LIMIT_PENALTY
            ) * 1000
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"message": "Rate limit exceeded. Please try after sometime."},
                headers={"Retry-After": str(RATE_LIMIT_WAIT_TIME)},
            )
    else:
        # else add to store
        localStore[clientIp] = {
            "count": 1,
            "last_request_time": currentTime * 1000,
        }

    response = await call_next(request)
    return response


@app.get("/")
async def Hello(request: Request):
    return "Hello World..."
