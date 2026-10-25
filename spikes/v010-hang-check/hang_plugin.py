import time


class HangingPlugin:
    """Sleeps in the request hook when the last message is exactly "hang"."""

    def process_request(self, request):
        if request["messages"][-1]["content"] == "hang":
            time.sleep(int(__import__("os").environ.get("HANG_SECONDS", "60")))
        return request

    def process_response(self, response):
        return response
