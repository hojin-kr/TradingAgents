import os
import sys
from datetime import datetime

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.simple_runner import run_and_save_reports


def main():
    ticker = os.environ.get("TA_TICKER", DEFAULT_CONFIG.get("ticker", "SPY"))
    analysis_date = os.environ.get(
        "TA_DATE", DEFAULT_CONFIG.get("analysis_date", datetime.now().strftime("%Y-%m-%d"))
    )

    # Minimal overrides: keep online_tools and quick model configurable
    config = DEFAULT_CONFIG.copy()
    if "TA_ONLINE_TOOLS" in os.environ:
        config["online_tools"] = os.environ["TA_ONLINE_TOOLS"].lower() in ("1", "true", "yes")
    if "TA_QUICK_LLM" in os.environ:
        config["quick_think_llm"] = os.environ["TA_QUICK_LLM"]

    outputs = run_and_save_reports(ticker, analysis_date, config=config, out_dir=os.environ.get("TA_OUT_DIR"))
    for key, path in outputs.items():
        print(f"{key} -> {path}")


if __name__ == "__main__":
    main()
