"""解题核心：封装 DeepSeek 调用，区分推理过程与最终解答。

DeepSeek 的 thinking 模式会在流式响应中分别返回：
  - delta.reasoning_content —— 模型的推理过程（对应"解题思路"）
  - delta.content           —— 面向用户的正式输出（对应"最终解答"）
"""
from __future__ import annotations

from functools import lru_cache
from typing import Iterator

from openai import OpenAI

from . import config

SYSTEM_PROMPT = """你是一位严谨的数学解题专家。请按以下要求解答用户给出的数学题目：

1. 先判断题目类型（代数、几何、应用题、概率、微积分等）。
2. 分步骤推导，每一步说明依据，逻辑清晰。
3. 所有数学公式使用 LaTeX 书写：行内公式用 \\( ... \\)，独立公式用 \\[ ... \\]。
4. 最后单独给出「最终答案」一节，并将关键结果用 \\boxed{ } 框出。
5. 若题目信息不足或无解，请明确指出原因。
使用简体中文作答。"""


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """返回模块级单例 DeepSeek 客户端（OpenAI 兼容）。"""
    return OpenAI(
        api_key=config.require_api_key(),
        base_url=config.DEEPSEEK_BASE_URL,
    )


def build_messages(problem: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": problem},
    ]


def _create_completion(problem: str, *, stream: bool):
    """统一的 DeepSeek 调用入口，便于测试时 mock。"""
    return get_client().chat.completions.create(
        model=config.DEEPSEEK_MODEL,
        messages=build_messages(problem),
        stream=stream,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )


def solve_stream(problem: str) -> Iterator[dict]:
    """流式解题：逐块产出 {"type": "reasoning"|"answer", "text": ...}。"""
    response = _create_completion(problem, stream=True)
    for chunk in response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        reasoning = getattr(delta, "reasoning_content", None)
        if reasoning:
            yield {"type": "reasoning", "text": reasoning}
        elif getattr(delta, "content", None):
            yield {"type": "answer", "text": delta.content}


def solve(problem: str) -> dict:
    """非流式解题：返回完整的 {"reasoning": ..., "answer": ...}。"""
    response = _create_completion(problem, stream=False)
    message = response.choices[0].message
    return {
        "reasoning": getattr(message, "reasoning_content", "") or "",
        "answer": message.content or "",
    }
