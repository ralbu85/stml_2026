"""W1 오프라인 테스트 — API 키·aisuite 설치 없이 chat() 배선을 검증한다.

가짜 aisuite 클라이언트를 docqa.llm._client 에 주입한다.
실행: pytest tests/test_week01.py -v
"""

import pytest

import docqa.llm as llm


class _FakeCompletions:
    def __init__(self, owner):
        self._owner = owner

    def create(self, **kwargs):
        self._owner.last_kwargs = kwargs

        class _Msg:
            content = "pong"

        class _Choice:
            message = _Msg()

        class _Resp:
            choices = [_Choice()]

        return _Resp()


class _FakeChat:
    def __init__(self, owner):
        self.completions = _FakeCompletions(owner)


class FakeClient:
    """aisuite Client와 같은 모양: client.chat.completions.create(...)"""

    def __init__(self):
        self.last_kwargs = None
        self.chat = _FakeChat(self)


@pytest.fixture
def fake_client():
    client = FakeClient()
    llm._client = client          # _get_client() 가 이걸 그대로 돌려준다
    yield client
    llm._client = None


def test_chat_returns_first_choice_content(fake_client):
    out = llm.chat([{"role": "user", "content": "ping"}])
    assert out == "pong"


def test_chat_uses_default_model_when_none(fake_client, monkeypatch):
    monkeypatch.setenv("DOCQA_MODEL", "openai:gpt-4o-mini")
    llm.chat([{"role": "user", "content": "ping"}])
    assert fake_client.last_kwargs["model"] == "openai:gpt-4o-mini"


def test_chat_respects_explicit_model_and_temperature(fake_client):
    llm.chat([{"role": "user", "content": "ping"}], model="ollama:llama3.2", temperature=0.7)
    assert fake_client.last_kwargs["model"] == "ollama:llama3.2"
    assert fake_client.last_kwargs["temperature"] == 0.7


def test_ask_builds_system_and_user_messages(fake_client):
    llm.ask("안녕", system="너는 조교다")
    messages = fake_client.last_kwargs["messages"]
    assert messages[0] == {"role": "system", "content": "너는 조교다"}
    assert messages[1] == {"role": "user", "content": "안녕"}
