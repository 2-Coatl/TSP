from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from src.db.base import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    translated_path = Column(String)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, default=func.now())
    status = Column(Enum('uploaded', 'translating', 'translated', name='document_status'), default='uploaded')
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', status='{self.status}')>"

    @classmethod
    def from_dict(cls, data):
        return cls(
            filename=data['filename'],
            file_path=data['file_path'],
            file_size=data['file_size'],
            source_language=data['source_language'],
            target_language=data['target_language']
        )

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_path': self.file_path,
            'translated_path': self.translated_path,
            'file_size': self.file_size,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'status': self.status,
            'source_language': self.source_language,
            'target_language': self.target_language
        }