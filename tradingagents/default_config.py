import os
from datetime import datetime

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "deep_think_llm": "o4-mini",
    "quick_think_llm": "gpt-4o-mini",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
    # Analysis settings
    "ticker": "SPY",  # Default ticker symbol
    "analysis_date": datetime.now().strftime("%Y-%m-%d"),  # Default analysis date
    "analysts": ["market", "social", "news", "fundamentals"],  # Default selected analysts
    "research_depth": 1,  # Default research depth
    "shallow_thinker": "gpt-4o-mini",  # Default shallow thinking model
    "deep_thinker": "o4-mini",  # Default deep thinking model
}
