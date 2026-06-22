"""共享的测试夹具与假对象，模拟 DeepSeek 响应结构。"""
import pytest


class FakeDelta:
    def __init__(self, reasoning_content=None, content=None):
        self.reasoning_content = reasoning_content
        self.content = content


class FakeChoice:
    def __init__(self, delta=None, message=None):
        self.delta = delta
        self.message = message


class FakeChunk:
    def __init__(self, delta):
        self.choices = [FakeChoice(delta=delta)]


class FakeMessage:
    def __init__(self, reasoning_content="", content=""):
        self.reasoning_content = reasoning_content
        self.content = content


class FakeCompletion:
    def __init__(self, message):
        self.choices = [FakeChoice(message=message)]


class FakeCompletions:
    """记录调用参数，并按 stream 返回流式块或完整响应。"""

    def __init__(self, stream_chunks, full_message):
        self.stream_chunks = stream_chunks
        self.full_message = full_message
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        if kwargs.get("stream"):
            return iter(self.stream_chunks)
        return FakeCompletion(self.full_message)


class FakeChat:
    def __init__(self, completions):
        self.completions = completions


class FakeClient:
    def __init__(self, completions):
        self.chat = FakeChat(completions)


@pytest.fixture
def fake_completions():
    chunks = [
        FakeChunk(FakeDelta(reasoning_content="先因式分解。")),
        FakeChunk(FakeDelta(reasoning_content="(x-2)(x-3)=0。")),
        FakeChunk(FakeDelta(content="最终答案：")),
        FakeChunk(FakeDelta(content="\\(x=2\\) 或 \\(x=3\\)。")),
        FakeChunk(FakeDelta()),  # 空块应被跳过
    ]
    message = FakeMessage(
        reasoning_content="先因式分解。(x-2)(x-3)=0。",
        content="最终答案：\\(x=2\\) 或 \\(x=3\\)。",
    )
    return FakeCompletions(chunks, message)


@pytest.fixture
def patched_solver(monkeypatch, fake_completions):
    """将 solver.get_client 替换为返回假客户端。"""
    from app import solver

    fake_client = FakeClient(fake_completions)
    monkeypatch.setattr(solver, "get_client", lambda: fake_client)
    return solver, fake_completions
