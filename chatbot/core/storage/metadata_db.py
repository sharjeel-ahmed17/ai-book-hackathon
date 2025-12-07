from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
import logging
from chatbot.config.settings import settings


logger = logging.getLogger(__name__)

Base = declarative_base()


class SessionModel(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now(), onupdate=func.now())
    metadata = Column(Text)  # JSON string


class QueryModel(Base):
    __tablename__ = "queries"

    query_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(Text)
    context_type = Column(String)
    selected_text = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())


class ResponseModel(Base):
    __tablename__ = "responses"

    response_id = Column(String, primary_key=True, index=True)
    query_id = Column(String, index=True)
    content = Column(Text)
    source_references = Column(Text)  # JSON string
    timestamp = Column(DateTime, default=func.now())
    validation_status = Column(String)


class MetadataDB:
    def __init__(self):
        self.engine = create_engine(
            settings.neon_database_url,
            pool_pre_ping=True,
            echo=False  # Set to True for debugging
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Session:
        """Get database session"""
        db = self.SessionLocal()
        try:
            return db
        except Exception as e:
            logger.error(f"Error getting database session: {e}")
            db.close()
            raise

    def create_session(self, session_id: str, user_id: Optional[str] = None, metadata: Optional[Dict] = None) -> bool:
        """Create a new conversation session"""
        db = self.get_db()
        try:
            session = SessionModel(
                session_id=session_id,
                user_id=user_id,
                metadata=str(metadata) if metadata else None
            )
            db.add(session)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by session_id"""
        db = self.get_db()
        try:
            session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
            if session:
                return {
                    "session_id": session.session_id,
                    "user_id": session.user_id,
                    "created_at": session.created_at,
                    "last_activity": session.last_activity,
                    "metadata": session.metadata
                }
            return None
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None
        finally:
            db.close()

    def create_query(self, query_id: str, session_id: str, content: str, context_type: str, selected_text: Optional[str] = None) -> bool:
        """Create a new query record"""
        db = self.get_db()
        try:
            query = QueryModel(
                query_id=query_id,
                session_id=session_id,
                content=content,
                context_type=context_type,
                selected_text=selected_text
            )
            db.add(query)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating query: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def create_response(self, response_id: str, query_id: str, content: str, source_references: List[Dict], validation_status: str) -> bool:
        """Create a new response record"""
        import json
        db = self.get_db()
        try:
            response = ResponseModel(
                response_id=response_id,
                query_id=query_id,
                content=content,
                source_references=json.dumps(source_references),
                validation_status=validation_status
            )
            db.add(response)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating response: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def get_response_by_query_id(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Get response by query_id"""
        import json
        db = self.get_db()
        try:
            response = db.query(ResponseModel).filter(ResponseModel.query_id == query_id).first()
            if response:
                return {
                    "response_id": response.response_id,
                    "query_id": response.query_id,
                    "content": response.content,
                    "source_references": json.loads(response.source_references) if response.source_references else [],
                    "timestamp": response.timestamp,
                    "validation_status": response.validation_status
                }
            return None
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return None
        finally:
            db.close()