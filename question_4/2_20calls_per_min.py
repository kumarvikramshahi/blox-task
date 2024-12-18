# It is practically impossible to make 20 API request per minute from single system if there is limit of 15 calls per minute.
# However we can achieve approx similar scenario by two ways:-
# 1. Bulk Requests: By making 15 call simultaneously(i.e. bulk call) and then waiting for 60 seconds to complete and after that make rest 5 calls. this will make 20 call at earliest without incurring penalties associated with exceeding the rate limit.
# 2. Using Proxy Servers: Another way is to use proxy server to make call. proxy server will make calls from different IP-addreses effectively bypassing rate limiting. We can use two different IPs that will be capable of making max 30 call per minute in total.

# Below is program of method 1:- Bulk Requests

import httpx
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "localhost:3000"
REQUEST_LIMIT_PER_MIN = 15
RATE_LIMIT_WAIT_TIME = 60  # sec


def makeCall(idx: int):
    print(f"call: ", idx)
    response = httpx.get(f"http://{URL}")
    if response.status_code != 200:
        print("Error response: ", response.json())
        return

    respData = response.json()
    print(respData)


def Make20ApiCall():
    # Using ThreadPoolExecutor to make 15 API calls concurrently
    with ThreadPoolExecutor(max_workers=15) as executor:
        futureToUrl = {executor.submit(makeCall, idx + 1): idx for idx in range(15)}

        for future in as_completed(futureToUrl):
            url = futureToUrl[future]
            try:
                _ = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")

    # sleep for 60 second
    time.sleep(RATE_LIMIT_WAIT_TIME)

    # make remaining API calls concurrently i.e. 5 calls
    with ThreadPoolExecutor(max_workers=5) as executor:
        futureToUrl = {executor.submit(makeCall, idx + 1): idx for idx in range(5)}

        for future in as_completed(futureToUrl):
            url = futureToUrl[future]
            try:
                _ = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")


if __name__ == "__main__":
    Make20ApiCall()
