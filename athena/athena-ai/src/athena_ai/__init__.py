"""Athena AI research assistant — REQ-AI-ASSISTANT-001."""

from athena_ai.application.research_assistant import ResearchAssistant
from athena_ai.domain.intent import ResearchIntent
from athena_ai.domain.research_plan import ResearchPlan, ResearchResult

__all__ = [
    "ResearchAssistant",
    "ResearchIntent",
    "ResearchPlan",
    "ResearchResult",
]
__version__ = "0.1.0"
