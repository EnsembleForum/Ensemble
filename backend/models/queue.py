"""
# Backend / Models / Queue
"""
from .tables import TQueue, TPost
from .post import Post
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.types.identifiers import QueueId
from backend.util.validators import assert_valid_str_field
from backend.types.queue import IQueueFullInfo
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

    def _get(self) -> TQueue:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TQueue, self.__id)

    @property
    def id(self) -> QueueId:
        """
        Identifier of the post
        """
        return self.__id

    # Create an empty list

    @classmethod
    def create(
        cls,
        queue_name: str,
    ) -> "Queue":
        assert_valid_str_field(queue_name, "queue_name")

        val = (
            TQueue(
                {
                    TQueue.queue_name: queue_name
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(QueueId, val["id"])
        return Queue(id)

    @property
    def queue_name(self) -> str:
        """
        Name of a
        """
        return self._get().queue_name

    @queue_name.setter
    def queue_name(self, queue_name: str):
        assert_valid_str_field(queue_name, "queue_name")
        row = self._get()
        row.queue_name = queue_name
        row.save().run_sync()

    # Get the list of all available queues
    @classmethod
    def all(cls) -> list["Queue"]:
        return [
            Queue(q["id"]) for q in
            TQueue.select().order_by(TQueue.queue_name, ascending=False)
            .run_sync()
        ]

    # Retrieve the posts for the queue specified
    # TODO: Revisit in sprint 2 to think of a way to organise
    @property
    def posts(self) -> list["Post"]:
        return [
            Post(c["id"])
            for c in TPost.select()
            .where(TPost.queue == self.__id)
            .order_by(TPost.id, ascending=False)
            .run_sync()
        ]

    # Remove a queue list
    # TODO: Complete routing in sprint 2
    def delete(cls, queue_id: QueueId) -> QueueId:
        TQueue.delete().where(TQueue.id == queue_id).run_sync()
        # Send posts back to original queue
        return queue_id

    @property
    def full_info(self) -> IQueueFullInfo:
        """
        Returns the full info of a post

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a post
        """
        return {
            "queue_name": self.queue_name,
            "posts": [c.id for c in self.posts],
        }
