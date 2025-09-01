from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from langchain_openai import ChatOpenAI

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.agents.analysts.social_media_analyst import (
    create_social_media_analyst,
)
from tradingagents.agents.analysts.news_analyst import create_news_analyst
from tradingagents.agents.analysts.fundamentals_analyst import (
    create_fundamentals_analyst,
)
from tradingagents.dataflows.interface import set_config


def _merge_configs(base: Dict[str, Any], overrides: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not overrides:
        return dict(base)
    merged = dict(base)
    merged.update(overrides)
    return merged


def _initialize_state(ticker: str, analysis_date: str) -> Dict[str, Any]:
    return {
        "messages": [("human", ticker)],
        "company_of_interest": ticker,
        "trade_date": str(analysis_date),
        "market_report": "",
        "fundamentals_report": "",
        "sentiment_report": "",
        "news_report": "",
    }


def _ensure_output_dir(base_dir: Path, ticker: str, analysis_date: str) -> Path:
    target = base_dir / ticker / analysis_date
    target.mkdir(parents=True, exist_ok=True)
    return target


def run_and_save_reports(
    ticker: str,
    analysis_date: str,
    config: Optional[Dict[str, Any]] = None,
    out_dir: Optional[str] = None,
) -> Dict[str, str]:
    """
    Run the four analysts (market, social, news, fundamentals) and save each
    generated report to a separate file. Returns a dict of agent->filepath.

    This function intentionally avoids the complex debate/graph pipeline and
    executes only the minimal steps required to produce per-agent reports.
    """

    merged_config = _merge_configs(DEFAULT_CONFIG, config)

    # Propagate configuration to dataflows layer for tools
    set_config(merged_config)

    # Use the quick thinking model for all analysts
    quick_llm = ChatOpenAI(model=merged_config["quick_think_llm"], temperature=0.1)
    toolkit = Toolkit(config=merged_config)

    # Prepare state shared across analysts
    state = _initialize_state(ticker, analysis_date)

    # Create analyst nodes
    market_node = create_market_analyst(quick_llm, toolkit)
    social_node = create_social_media_analyst(quick_llm, toolkit)
    news_node = create_news_analyst(quick_llm, toolkit)
    fundamentals_node = create_fundamentals_analyst(quick_llm, toolkit)

    # Execute analysts sequentially; each returns deltas to merge into state
    for node in (market_node, social_node, news_node, fundamentals_node):
        result_delta = node(state)
        # Merge new messages and report fields into state
        if "messages" in result_delta:
            state["messages"] = state.get("messages", []) + result_delta["messages"]
        for key in ("market_report", "sentiment_report", "news_report", "fundamentals_report"):
            if key in result_delta:
                state[key] = result_delta[key]

    # Determine output directory
    base_output = Path(out_dir or "agent_reports")
    output_dir = _ensure_output_dir(base_output, ticker, analysis_date)

    # Save each report to an individual markdown file
    outputs: Dict[str, str] = {}
    report_mapping: Tuple[Tuple[str, str], ...] = (
        ("market_report", "market.md"),
        ("sentiment_report", "social.md"),
        ("news_report", "news.md"),
        ("fundamentals_report", "fundamentals.md"),
    )

    for state_key, filename in report_mapping:
        content = state.get(state_key, "")
        file_path = output_dir / filename
        with open(file_path, "w") as f:
            f.write(content or "")
        outputs[state_key] = str(file_path)

    return outputs

