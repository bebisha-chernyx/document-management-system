from abc import ABC, abstractmethod


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document):
        pass

    @abstractmethod
    def find_by_filename(self, filename):
        pass

    @abstractmethod
    def find_by_hash(self, file_hash):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def delete(self, document_id):
        pass