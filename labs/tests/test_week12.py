"""W12 오프라인 테스트 — tools_web (네트워크 없이 가짜 응답 주입).
실행: pytest tests/test_week12.py -v"""

import pytest

from docqa import tools_web


class FakeResp:
    def __init__(self, text, status=200):
        self.text = text
        self._status = status

    def raise_for_status(self):
        if self._status >= 400:
            raise RuntimeError(f"HTTP {self._status}")


def test_strip_html():
    html = "<html><script>evil()</script><body><h1>제목</h1><p>본문 텍스트</p></body></html>"
    out = tools_web._strip_html(html)
    assert "본문 텍스트" in out and "evil" not in out and "<" not in out


def test_fetch_url_returns_text(monkeypatch):
    monkeypatch.setattr(tools_web.requests, "get",
                        lambda *a, **kw: FakeResp("<p>안녕 웹</p>"))
    assert "안녕 웹" in tools_web.fetch_url("https://example.com")


def test_fetch_url_truncates(monkeypatch):
    monkeypatch.setattr(tools_web.requests, "get",
                        lambda *a, **kw: FakeResp("<p>" + "x" * 10_000 + "</p>"))
    out = tools_web.fetch_url("https://example.com")
    assert len(out) <= tools_web.MAX_CHARS + 20 and "잘림" in out


def test_fetch_url_raises_on_http_error(monkeypatch):
    """예외는 잡지 않는다 — W4 run_tool이 관찰로 바꿔줄 것."""
    monkeypatch.setattr(tools_web.requests, "get",
                        lambda *a, **kw: FakeResp("", status=404))
    with pytest.raises(Exception):
        tools_web.fetch_url("https://example.com/none")
