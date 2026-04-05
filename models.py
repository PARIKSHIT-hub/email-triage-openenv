from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any, List
from uuid import uuid4


class EmailObservation(BaseModel):
    # OpenEnv required fields
    reward: float = 0.0
    done: bool = False

    # Email-specific fields
    email_id: str = ""
    subject: str = ""
    sender: str = ""
    body_snippet: str = ""
    timestamp: str = ""
    thread_id: Optional[str] = None
    sender_reputation: float = Field(0.5, ge=0.0, le=1.0)
    is_time_sensitive: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TriageAction(BaseModel):
    category: Literal["work", "personal", "spam", "urgent", "promo"]
    priority: Literal["high", "medium", "low"]
    action_type: Literal["archive", "reply", "forward", "route_to_folder", "escalate_to_human", "noop"]
    folder: Optional[str] = None
    reply_draft: Optional[str] = None
    forward_to: Optional[str] = None


class EnvironmentState(BaseModel):
    episode_id: str = Field(default_factory=lambda: str(uuid4()))
    step_count: int = 0
    emails_processed: int = 0
    task_name: str = "easy"
    attention_budget_remaining: int = 8
    processed_emails: List[str] = Field(default_factory=list)


# Aliases so root __init__.py imports work correctly
EmailTriageAction = TriageAction
EmailTriageObservation = EmailObservation