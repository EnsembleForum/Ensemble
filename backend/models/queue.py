"""
# Backend / Models / Queue
"""
from .tables import TQueue, TPost
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.types.identifiers import QueueId
from backend.util.validators import assert_valid_str_field
from backend.util import http_errors
from backend.types.queue import IQueueFullInfo, IQueueBasicInfo
from typing import cast, TYPE_CHECKING
if TYPE_CHECKING:
    from .post import Post


class Queue:
    """
    Represents a queue
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
        name: str,
        immutable: bool = False,
    ) -> "Queue":
        """
        Create a new queue and save it to the database

        ### Args:
        * `queue_name` (`str`): name of queue
        * `immutable` (`bool`): default false (not immutable). it determines
           whether the queue is changeable or not

        ### Returns:
        * `Queue`: the new queue
        """
        assert_valid_str_field(name, "queue_name")

        if name in [q.name for q in cls.all()]:
            raise http_errors.BadRequest(
                "There is already a queue with that name")

        val = (
            TQueue(
                {
                    TQueue.name: name,
                    TQueue.immutable: immutable
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(QueueId, val["id"])
        return Queue(id)

    @property
    def name(self) -> str:
        """
        Name of the queue
        """
        return self._get().name

    @name.setter
    def name(self, new_name: str):
        assert_valid_str_field(new_name, "queue_name")
        row = self._get()
        row.name = new_name
        row.save().run_sync()

    @classmethod
    def all(cls) -> list["Queue"]:
        """
        Get the list of all available queues
        """
        # IDEA: custom ordering of queues in the future
        return [
            Queue(q.id) for q in TQueue.objects()
            .order_by(TQueue.name, ascending=False).run_sync()]

    @classmethod
    def get_main_queue(cls) -> "Queue":
        """
        Gets the main queue

        ### Returns:
        * `queue`: main queue
        """
        q = TQueue.objects()\
            .where(TQueue.immutable.eq(True)).first().run_sync()
        return Queue(q.id)

    # TODO: Revisit in sprint 2 to think of a way to organise
    def posts(self) -> list["Post"]:
        """
        List of all posts in the given queue

        ### Returns:
        * `list[Post]`: posts
        """
        from .post import Post
        return [
            Post(c["id"])
            for c in TPost.select()
            .where(TPost.queue == self.id)
            .order_by(TPost.id, ascending=False)
            .run_sync()
        ]

    def delete(self) -> None:
        """
        Delete a queue

        This should move all post back into the main queue
        """
        # Error checking (can't delete main queue)
        row = self._get()
        if row.immutable:
            raise http_errors.BadRequest('Cannot delete main queue')
        # Send posts back to original queue
        main_queue = self.get_main_queue()
        for p in self.posts():
            p.queue = main_queue
        TQueue.delete().where(TQueue.id == self.id).run_sync()

    def full_info(self) -> IQueueFullInfo:
        """
        Returns the full info of a queue

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a queue
        """
        return {
            "queue_id": self.id,
            "queue_name": self.name,
            "posts": [c.id for c in self.posts()],
        }

    def basic_info(self) -> IQueueBasicInfo:
        """
        Returns the basic info of a queue

        ### Returns:
        * IPostBasicInfo: Dictionary containing full info a queue
        """
        return {
            "queue_id": self.id,
            "queue_name": self.name,
        }
