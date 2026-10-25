"""Importable synthetic plugins; these exercise real spawned workers."""

import os
import signal
import time


class Passthrough:
    def process_request(self, request):
        return request

    def process_response(self, response):
        return response


class SlowRequest(Passthrough):
    def process_request(self, request):
        if request["messages"][-1]["content"] == "sleep":
            time.sleep(5)
        return request


class SlowResponse(Passthrough):
    def process_request(self, request):
        self.slow = request["messages"][-1]["content"] == "sleep"
        return request

    def process_response(self, response):
        if self.slow:
            time.sleep(5)
        return response


class BusyLoop(Passthrough):
    def process_request(self, request):
        if request["messages"][-1]["content"] == "spin":
            while True:
                pass
        return request


class SlightlySlow(Passthrough):
    def process_request(self, request):
        time.sleep(0.3)
        return request


class IgnoreTerminate(Passthrough):
    def process_request(self, request):
        if request["messages"][-1]["content"] == "sleep":
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            time.sleep(5)
        return request


class ExitWorker(Passthrough):
    def process_request(self, request):
        if request["messages"][-1]["content"] == "exit":
            os._exit(17)
        return request


class SystemExitPlugin(Passthrough):
    def process_request(self, request):
        if request["messages"][-1]["content"] == "exit":
            raise SystemExit("DO_NOT_LOG_SYSTEM_EXIT")
        return request


class MalformedRequest(Passthrough):
    def process_request(self, request):
        mode = request["messages"][-1]["content"]
        if mode == "none":
            return None
        if mode == "messages":
            request["messages"] = "invalid"
        elif mode == "trace":
            request["plugin_trace"] = {"not": "a list"}
        elif mode == "json":
            request["unexpected"] = object()
        elif mode == "large":
            request["unexpected"] = "x" * (1024 * 1024)
        return request


class MalformedResponse(Passthrough):
    def process_response(self, response):
        response["choices"] = [{"message": None}]
        return response


class RequestState(Passthrough):
    def __init__(self):
        self.calls = 0

    def process_request(self, request):
        self.calls += 1
        self.message = request["messages"][-1]["content"]
        return request

    def process_response(self, response):
        response["choices"][0]["message"]["content"] = f"{self.message}:{self.calls}"
        return response
