# We can use API within the safe limit by using caching.
# Before sending each request check when we have made last API request and how many requests in last 60 seconds. if we have exceeded limit then abort HTTP request.
# By using this strategy we can prevent ourselves from 1 min extra penalty.
# Below is the program for same.

import httpx
from datetime import datetime


REQUEST_LIMIT_PER_MIN = 15
RATE_LIMIT_WAIT_TIME = 60  # sec

requestCount = 0
lastRequestTime = 0  # epoch time in millisecond
URL = "localhost:3000"


def MakeApiCall():
    global requestCount
    global lastRequestTime
    currentTime = datetime.now().timestamp()
    lastRequestTime = lastRequestTime / 1000

    if currentTime - lastRequestTime <= RATE_LIMIT_WAIT_TIME:
        requestCount += 1
        lastRequestTime = currentTime * 1000
        if requestCount > REQUEST_LIMIT_PER_MIN:
            print(
                "Http call aborted due to exceeding rate limit.. Please try after sometime."
            )
            return
    else:
        # else add to store
        requestCount = 1
        lastRequestTime = currentTime * 1000

    # make api call now
    response = httpx.get(f"http://{URL}")
    if response.status_code != 200:
        print("Error response: ", response.json())
        return

    respData = response.json()
    print(respData)


if __name__ == "__main__":
    print(f"Making {REQUEST_LIMIT_PER_MIN+1} HTTP calls to Rate limiter API")

    for i in range(REQUEST_LIMIT_PER_MIN + 2):
        MakeApiCall()
