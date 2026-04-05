# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Email Triage Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from models import TriageAction, EmailObservation


class EmailTriageEnv(
    EnvClient[TriageAction, EmailObservation, State]
):
    """
    Client for the Email Triage Environment.

    Example:
        >>> with EmailTriageEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     result = client.step(TriageAction(
        ...         category="work",
        ...         priority="high",
        ...         action_type="reply"
        ...     ))
    """

    def _step_payload(self, action: TriageAction) -> Dict:
        """Convert TriageAction to JSON payload for step message."""
        return action.model_dump()

    def _parse_result(self, payload: Dict) -> StepResult[EmailObservation]:
        """Parse server response into StepResult[EmailObservation]."""
        obs_data = payload.get("observation", {})
        observation = EmailObservation(
            email_id=obs_data.get("email_id", ""),
            subject=obs_data.get("subject", ""),
            sender=obs_data.get("sender", ""),
            body_snippet=obs_data.get("body_snippet", ""),
            timestamp=obs_data.get("timestamp", ""),
            thread_id=obs_data.get("thread_id"),
            sender_reputation=obs_data.get("sender_reputation", 0.5),
            is_time_sensitive=obs_data.get("is_time_sensitive", False),
            done=obs_data.get("done", False),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """Parse server response into State object."""
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )