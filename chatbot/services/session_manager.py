from typing import Dict, Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from chatbot.core.models.conversation_session import ConversationSession, QueryInSession
from chatbot.core.storage.metadata_db import MetadataDB


class SessionManager:
    """Manages conversation sessions and their state"""

    def __init__(self, metadata_db: MetadataDB):
        self.metadata_db = metadata_db
        self.active_sessions: Dict[str, ConversationSession] = {}

    def create_session(self, user_id: Optional[str] = None) -> ConversationSession:
        """Create a new conversation session"""
        session_id = str(uuid4())

        # Create in database
        success = self.metadata_db.create_session(session_id, user_id)
        if not success:
            raise Exception("Failed to create session in database")

        # Create session object
        session = ConversationSession(
            session_id=uuid4(),
            user_id=uuid4() if user_id else None,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            queries=[],
            metadata=None  # Will be populated as needed
        )

        # Store in active sessions
        self.active_sessions[session_id] = session

        return session

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get an existing conversation session"""
        # First check active sessions
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]

        # Then check database
        session_data = self.metadata_db.get_session(session_id)
        if session_data:
            # Create a ConversationSession object from the database data
            session = ConversationSession(
                session_id=UUID(session_data["session_id"]),
                user_id=UUID(session_data["user_id"]) if session_data["user_id"] else None,
                created_at=session_data["created_at"],
                last_activity=session_data["last_activity"],
                queries=[],  # We might want to load queries as well
                metadata=session_data["metadata"]
            )
            # Cache in active sessions
            self.active_sessions[session_id] = session
            return session

        return None

    def add_query_to_session(self, session_id: str, query_id: str) -> bool:
        """Add a query to a session"""
        session = self.get_session(session_id)
        if not session:
            return False

        query_in_session = QueryInSession(
            query_id=UUID(query_id),
            timestamp=datetime.now()
        )

        session.queries.append(query_in_session)
        session.last_activity = datetime.now()

        # Update in active sessions cache
        self.active_sessions[session_id] = session

        return True

    def end_session(self, session_id: str) -> bool:
        """End a session and remove from active sessions"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False

    def get_recent_queries(self, session_id: str, limit: int = 5) -> List[QueryInSession]:
        """Get recent queries from a session"""
        session = self.get_session(session_id)
        if session:
            return session.queries[-limit:] if len(session.queries) >= limit else session.queries
        return []

    def update_session_metadata(self, session_id: str, metadata: Dict) -> bool:
        """Update session metadata"""
        session = self.get_session(session_id)
        if not session:
            return False

        # In a real implementation, you might want to merge metadata rather than replace
        session.metadata = metadata
        session.last_activity = datetime.now()

        # Update in active sessions cache
        self.active_sessions[session_id] = session

        # Also update in database
        # This would require an update method in MetadataDB
        return True