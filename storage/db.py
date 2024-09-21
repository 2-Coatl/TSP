from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('uploaded', 'translating', 'translated', name='document_status'), default='uploaded')
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)

class DatabaseManager:
    def __init__(self):
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/mydatabase')
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_document(self, filename, file_path, file_size, source_language, target_language):
        with self.SessionLocal() as session:
            new_doc = Document(
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                source_language=source_language,
                target_language=target_language
            )
            session.add(new_doc)
            session.commit()
            return new_doc.id

    def get_document(self, doc_id):
        with self.SessionLocal() as session:
            return session.query(Document).filter(Document.id == doc_id).first()

    def update_document_status(self, doc_id, new_status):
        with self.SessionLocal() as session:
            doc = session.query(Document).filter(Document.id == doc_id).first()
            if doc:
                new_doc = Document(
                    filename=doc.filename,
                    file_path=doc.file_path,
                    file_size=doc.file_size,
                    upload_date=doc.upload_date,
                    status=new_status,
                    source_language=doc.source_language,
                    target_language=doc.target_language
                )
                session.add(new_doc)
                session.commit()
                return new_doc.id
            return None

    def get_documents_for_translation(self):
        with self.SessionLocal() as session:
            return session.query(Document).filter(Document.status == 'uploaded').all()