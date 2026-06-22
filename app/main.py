"""FastAPI 应用：网页、非流式解题、SSE 流式解题。"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import solver
from .schemas import SolveRequest, SolveResponse

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="智能数学解题智能体")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/solve", response_model=SolveResponse)
def api_solve(req: SolveRequest) -> SolveResponse:
    result = solver.solve(req.problem)
    return SolveResponse(**result)


@app.get("/api/solve/stream")
def api_solve_stream(problem: str) -> StreamingResponse:
    def event_source():
        try:
            for piece in solver.solve_stream(problem):
                yield f"data: {json.dumps(piece, ensure_ascii=False)}\n\n"
        except Exception as exc:  # noqa: BLE001 — 把错误透传给前端展示
            err = {"type": "error", "text": str(exc)}
            yield f"data: {json.dumps(err, ensure_ascii=False)}\n\n"
        yield 'data: {"type": "done"}\n\n'

    return StreamingResponse(event_source(), media_type="text/event-stream")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
