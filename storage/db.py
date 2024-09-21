import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utils.decorators import handle_error
from utils.logger import LoggerManager

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    translated_path = Column(String)  # New field for translated document path
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

    @handle_error
    def create_tables(self):
        Base.metadata.create_all(self.engine)
        LoggerManager.log_message("Database tables created", level='info')

    @handle_error
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
            LoggerManager.log_message(f"Document added to database: {filename}", level='info')
            return new_doc.id

    @handle_error
    def get_document(self, doc_id):
        with self.SessionLocal() as session:
            doc = session.query(Document).filter(Document.id == doc_id).first()
            if doc:
                LoggerManager.log_message(f"Retrieved document: {doc_id}", level='info')
            else:
                LoggerManager.log_message(f"Document not found: {doc_id}", level='warning')
            return doc

    @handle_error
    def update_document_status(self, doc_id, new_status):
        with self.SessionLocal() as session:
            doc = session.query(Document).filter(Document.id == doc_id).first()
            if doc:
                doc.status = new_status
                session.commit()
                LoggerManager.log_message(f"Updated document status: {doc_id} to {new_status}", level='info')
                return True
            LoggerManager.log_message(f"Failed to update document status: {doc_id}", level='warning')
            return False

    @handle_error
    def update_document_translated_path(self, doc_id, translated_path):
        with self.SessionLocal() as session:
            doc = session.query(Document).filter(Document.id == doc_id).first()
            if doc:
                doc.translated_path = translated_path
                doc.status = 'translated'
                session.commit()
                LoggerManager.log_message(f"Updated translated path for document: {doc_id}", level='info')
                return True
            LoggerManager.log_message(f"Failed to update translated path for document: {doc_id}", level='warning')
            return False

    @handle_error
    def get_documents_for_translation(self):
        with self.SessionLocal() as session:
            docs = session.query(Document).filter(Document.status == 'uploaded').all()
            LoggerManager.log_message(f"Retrieved {len(docs)} documents for translation", level='info')
            return docs