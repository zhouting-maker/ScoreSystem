"""请求 / 响应数据模型。"""
from pydantic import BaseModel, Field


class SolveRequest(BaseModel):
    problem: str = Field(..., min_length=1, description="数学题目文本")


class SolveResponse(BaseModel):
    reasoning: str = Field("", description="解题思路（推理过程）")
    answer: str = Field("", description="最终解答")
