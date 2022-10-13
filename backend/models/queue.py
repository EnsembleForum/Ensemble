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
        Identifier of the queue
        """
        return self.__id

    @classmethod
    def create(
        cls,
        queue_name: str,
    ) -> "Queue":
        """
        Create a new queue and save it to the database

        ### Args:
        * `queue_name` (`str`): name of queue

        ### Returns:
        * `Queue`: the new queue
        """
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
    def queue(self) -> str:
        """
        Name of the queue
        """
        return self._get().queue_name

    @queue.setter
    def queue(self, queue_name: str):
        assert_valid_str_field(queue_name, "queue_name")
        row = self._get()
        row.queue_name = queue_name
        row.save().run_sync()

    @classmethod
    def all(cls) -> list["Queue"]:
        """
        Get the list of all available queues
        """
        return [
            Queue(q["id"]) for q in
            TQueue.select().order_by(TQueue.queue_name, ascending=False)
            .run_sync()
        ]

    # TODO: Revisit in sprint 2 to think of a way to organise
    @property
    def posts(self) -> list["Post"]:
        """
        List of all posts in the given queue

        ### Returns:
        * `list[Post]`: posts
        """
        return [
            Post(c["id"])
            for c in TPost.select()
            .where(TPost.queue == self.__id)
            .order_by(TPost.id, ascending=False)
            .run_sync()
        ]

    def delete(self) -> None:
        """
        Delete a queue

        This should move all post back into the main queue
        """
        # TODO: Error checking (can't delete main queue)
        TQueue.delete().where(TQueue.id == self.id).run_sync()
        # TODO: Send posts back to original queue

    def full_info(self) -> IQueueFullInfo:
        """
        Returns the full info of a post

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a post
        """
        return {
            "queue_name": self.queue,
            "posts": [c.id for c in self.posts],
        }
