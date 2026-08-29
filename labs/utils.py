"""노트북용 표시 헬퍼 — 대화 메시지와 응답을 박스로 렌더링한다.

노트북에서는 HTML 박스, 터미널에서는 구분선 있는 텍스트로 출력한다.
구성 참조: Andrew Ng *Agentic AI* 랩의 utils.print_html / show_output.
"""

from __future__ import annotations

ROLE_COLORS = {
    "system": "#fff8dc",
    "user": "#e0f7fa",
    "assistant": "#f3e5f5",
    "tool": "#e8f5e9",
}
DEFAULT_COLOR = "#f5f5f5"


def _display_html(html: str) -> bool:
    """IPython 환경이면 HTML을 렌더링하고 True, 아니면 False. (내부용)"""
    try:
        from IPython.display import HTML, display
        display(HTML(html))
        return True
    except ImportError:
        return False


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def show_box(title: str, text: str, color: str = DEFAULT_COLOR) -> None:
    """제목 달린 박스 하나에 텍스트를 표시한다."""
    html = (
        f'<div style="background:{color}; color:#222; border:1px solid #ccc; '
        f'border-radius:6px; padding:10px 14px; margin:6px 0; font-size:14px;">'
        f"<b>{_escape(title)}</b>"
        f'<pre style="white-space:pre-wrap; margin:6px 0 0 0; font-size:13px; '
        f'background:transparent; color:inherit;">{_escape(text)}</pre></div>'
    )
    if not _display_html(html):
        line = "─" * 50
        print(f"{line}\n[{title}]\n{text}\n{line}")


def show_messages(messages: list[dict]) -> None:
    """messages 목록을 역할별 색 박스로 순서대로 표시한다."""
    for m in messages:
        role = m.get("role", "?")
        show_box(role, m.get("content", ""), ROLE_COLORS.get(role, DEFAULT_COLOR))
