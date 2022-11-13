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
        view_only: bool = False,
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
                    TQueue.immutable: immutable,
                    TQueue.view_only: view_only
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(QueueId, val["id"])
        return Queue(id)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Queue):
            return self.id == __o.id
        else:
            return False

    @property
    def name(self) -> str:
        """
        Name of the queue
        """
        return self._get().name

    @name.setter
    def name(self, new_name: str):
        assert_valid_str_field(new_name, "queue_name")
        if new_name in [q.name for q in self.all() if q.id != self.id]:
            raise http_errors.BadRequest(
                "There is already a queue with that name")
        row = self._get()
        row.name = new_name
        row.save().run_sync()

    @property
    def view_only(self) -> bool:
        """
        Whether we can move posts to and from this queue in the taskboard page
        """
        return self._get().view_only

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
    def get_queue(cls, queue_name: str) -> "Queue":
        q = TQueue.objects()\
            .where(TQueue.name == queue_name).first().run_sync()
        return Queue(q.id)

    @classmethod
    def get_main_queue(cls) -> "Queue":
        """
        Gets the main queue

        ### Returns:
        * `queue`: main queue
        """
        # TODO: Remember not to use duplicate queue names otherwise this breaks
        return cls.get_queue("Main queue")

    @classmethod
    def get_answered_queue(cls) -> "Queue":
        """
        Gets the answered queue

        ### Returns:
        * `queue`: answered queue
        """
        # TODO: Remember not to use duplicate queue names otherwise this breaks
        return cls.get_queue("Answered queue")

    @classmethod
    def get_closed_queue(cls) -> "Queue":
        """
        Gets the closed queue

        ### Returns:
        * `queue`: closed queue
        """
        # TODO: Remember not to use duplicate queue names otherwise this breaks
        return cls.get_queue("Closed queue")

    @classmethod
    def get_deleted_queue(cls) -> "Queue":
        """
        Gets the deleted queue

        ### Returns:
        * `queue`: deleted queue
        """
        # TODO: Remember not to use duplicate queue names otherwise this breaks
        return cls.get_queue("Deleted queue")

    def posts(self) -> list["Post"]:
        """
        List of all posts in the given queue
        Posts are sorted from oldest to newest

        ### Returns:
        * `list[Post]`: posts
        """
        from .post import Post
        return [
            Post(c["id"])
            for c in TPost.select()
            .where(TPost.queue == self.id)
            .order_by(TPost.id, ascending=True)
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
            "view_only": self.view_only,
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
            "view_only": self.view_only,
        }
