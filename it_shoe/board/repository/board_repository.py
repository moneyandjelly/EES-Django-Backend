from abc import ABC, abstractmethod


class BoardRepository(ABC):
    @abstractmethod
    def create_board(self, board):
        pass