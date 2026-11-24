"""정비 시스템 MCP 서버 maint-tools — 현대화한 기능을 '필요한 것만, 필요한 범위만' 도구로 공개한다.

실행은 에이전트가 한다 (stdio). 직접 실행하면 입력을 기다리며 멈춘다.
※ mcp 1.x 기준 (mcp 2.x에서는 FastMCP가 MCPServer로 바뀜)
"""

import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ.setdefault("MAINT_DB", str(HERE / "data" / "maintenance.db"))

from mcp.server.fastmcp import FastMCP  # noqa: E402

import app  # noqa: E402

mcp = FastMCP("maint-tools")


@mcp.tool()
def recall_targets(code: str) -> list[str]:
    """리콜 코드(예: R2024-01)를 받아, 리콜 대상인데 아직 조치하지 않은 차량번호 목록을 돌려준다.

    리콜 미조치 차량, 리콜 대상 차량을 물을 때 쓴다. 고객 정보는 돌려주지 않는다.
    """
    return app.find_recall_targets(code)


@mcp.tool()
def recall_status(code: str) -> dict | None:
    """리콜 코드의 진행 현황(대상 대수, 조치 완료, 남은 대수, 조치율 %)을 돌려준다. 없는 코드면 None.

    리콜이 얼마나 진행됐는지, 조치율을 물을 때 쓴다. 조치율은 버림이다 (2/3 → 66).
    """
    return app.recall_status(code)


@mcp.tool()
def vehicle_history(plate: str) -> list[dict]:
    """차량번호(예: 12가3456)의 정비 이력(날짜, 주행거리, 작업, 비용)을 최신순으로 돌려준다.

    특정 차량의 정비 기록, 최근 정비를 물을 때 쓴다. 고객 개인정보는 포함하지 않는다.
    """
    return app.get_history(plate)


if __name__ == "__main__":
    mcp.run()
