from abc import ABC, abstractmethod
from typing import Optional


class TaskRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, task_id: int):
        pass

    @abstractmethod
    def create(self, title: str):
        pass

    @abstractmethod
    def update(self, task_id: int, title: str):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass