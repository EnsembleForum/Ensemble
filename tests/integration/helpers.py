"""
# Tests / Integration / Helpers

Helpers for making testing easier
"""
from backend.types.queue import IQueueBasicInfo


def get_queue(
        queues: list[IQueueBasicInfo],
        queue_name: str) -> IQueueBasicInfo | None:
    for q in queues:
        if q["queue_name"] == queue_name:
            return q
    return None
