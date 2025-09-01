import os
import typer
from datetime import datetime

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.simple_runner import run_and_save_reports


app = typer.Typer(help="TradingAgents minimal CLI: generate per-agent reports and save to files")


@app.command()
def run(
    ticker: str = typer.Option(DEFAULT_CONFIG.get("ticker", "SPY"), help="Ticker symbol"),
    date: str = typer.Option(DEFAULT_CONFIG.get("analysis_date", datetime.now().strftime("%Y-%m-%d")), help="Analysis date YYYY-MM-DD"),
    out_dir: str = typer.Option("agent_reports", help="Output directory base"),
    quick_llm: str = typer.Option(DEFAULT_CONFIG.get("quick_think_llm", "gpt-4o-mini"), help="Model name for quick thinking LLM"),
    online_tools: bool = typer.Option(True, help="Enable online tools"),
):
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = quick_llm
    config["online_tools"] = online_tools

    outputs = run_and_save_reports(ticker, date, config=config, out_dir=out_dir)
    for key, path in outputs.items():
        typer.echo(f"{key}: {path}")


if __name__ == "__main__":
    app()

