"""
# Backend / Models / Queue
"""
from .tables import TQueue, TPost
from .post import Post
from backend.util.db_queries import assert_id_exists
from backend.types.identifiers import QueueId
from backend.util.validators import assert_valid_str_field
from typing import cast

class Queue:
    """
    Represents a queues in Ensemble
    """

    def __init__(self, id: QueueId):
        """
        Create a queue object


        ### Args:
        * `id` (`int`): queue id

        ### Raises:
        `IdNotFound`: queue does not exist
        """
        assert_id_exists(TQueue, id, "Queue")
        self.__id = id

    # Create an empty list
    @classmethod
    def create(
        cls,
        heading: str,
    ) -> "Queue":
        assert_valid_str_field(heading, "heading")

        val = (
            TQueue(
                {
                    TQueue.heading: heading
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(QueueId, val["id"])
        return Queue(id)

    #Get the list of all available queues
    @classmethod
    def all(cls) -> list["Queue"]:
        return [
            Queue(q["id"]) for q in
            TQueue.select().order_by(TQueue.id, ascending=False).run_sync()
        ]

    @property
    def posts(self) -> list["Post"]:
        return [
            Post(c["id"])
            for c in TPost.select()
            .where(TPost.id == self.__id)
            .order_by(TPost.id, ascending=False)
            .run_sync()
        ]
    # Remove a queue list
    # Sending any posts within the queue back to the main queue
    @classmethod
    def delete(cls, queue_id: QueueId) -> QueueId:
        TQueue.delete().where(TQueue.id == queue_id).run_sync()
        # Send posts back to original queue
        return queue_id

    # Getter?
    # Retrieve the posts for the queue specified

    # Add a post to this queue (remove it from its original queue)




