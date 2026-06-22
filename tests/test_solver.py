"""solver 模块单元测试（不调用真实 API）。"""
from app import config, solver


def test_build_messages_includes_system_prompt():
    messages = solver.build_messages("求 1+1")
    assert messages[0]["role"] == "system"
    assert "数学" in messages[0]["content"]
    assert messages[1] == {"role": "user", "content": "求 1+1"}


def test_solve_splits_reasoning_and_answer(patched_solver):
    solver_mod, _ = patched_solver
    result = solver_mod.solve("解方程 x² - 5x + 6 = 0")
    assert "因式分解" in result["reasoning"]
    assert "x=2" in result["answer"]


def test_solve_stream_yields_typed_pieces(patched_solver):
    solver_mod, _ = patched_solver
    pieces = list(solver_mod.solve_stream("解方程 x² - 5x + 6 = 0"))
    types = [p["type"] for p in pieces]
    assert "reasoning" in types
    assert "answer" in types
    # 空块（无 reasoning 也无 content）应被跳过
    assert all(p["text"] for p in pieces)


def test_create_completion_enables_thinking(patched_solver):
    solver_mod, fake_completions = patched_solver
    solver_mod.solve("任意题目")
    kwargs = fake_completions.last_kwargs
    assert kwargs["model"] == config.DEEPSEEK_MODEL
    assert kwargs["extra_body"] == {"thinking": {"type": "enabled"}}
    assert kwargs["stream"] is False
