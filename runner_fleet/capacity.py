from __future__ import annotations

import math

from .models import CapacityRecommendation, CapacityRequest


def recommend_capacity(request: CapacityRequest) -> CapacityRecommendation:
    if request.queued_jobs == 0:
        desired = max(0, request.current_runners)
        return CapacityRecommendation(
            desired_runners=desired,
            additional_runners=0,
            capped=False,
            rationale="No queued jobs require additional capacity.",
        )

    jobs_per_runner_in_target = max(
        1, request.target_queue_seconds / request.average_job_seconds
    )
    required_for_queue = math.ceil(request.queued_jobs / jobs_per_runner_in_target)
    desired = max(request.current_runners, required_for_queue)
    capped = desired > request.maximum_runners
    desired = min(desired, request.maximum_runners)
    return CapacityRecommendation(
        desired_runners=desired,
        additional_runners=max(0, desired - request.current_runners),
        capped=capped,
        rationale=(
            "Estimate uses queue depth, average job duration, and the queue-time "
            "target. It is advisory and does not mutate runner capacity."
        ),
    )
