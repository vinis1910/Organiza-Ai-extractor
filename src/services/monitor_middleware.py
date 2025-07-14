# monitor_middleware.py
import time, psutil, os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

process = psutil.Process(os.getpid())


class ResourceMonitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cpu_start = process.cpu_times().user
        mem_start = process.memory_info().rss
        wall_start = time.perf_counter()

        response = await call_next(request)

        wall_elapsed = (time.perf_counter() - wall_start) * 1000
        cpu_elapsed = process.cpu_times().user - cpu_start
        mem_end = process.memory_info().rss
        mem_diff_mb = (mem_end - mem_start) / (1024 * 1024)
        mCPU = (cpu_elapsed / wall_elapsed) * 1000
        endpoint = request.url.path
        print(f"[{endpoint}] wall={wall_elapsed:.1f} ms  " f"cpu={cpu_elapsed*1000:.1f} ms  " f"cpu mCPU={mCPU:.1f} " f"∆RSS={mem_diff_mb:.2f} MB")
        return response
