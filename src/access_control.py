from typing import Dict

class AccessControl:
    def __init__(self):
        self.user_levels: Dict[str, int] = {}       # Maps user_id to their access level
        self.document_levels: Dict[str, int] = {}   # Maps doc_id to required access level

    def add_user(self, user_id: str, level: int) -> None:
        """Add a user with a specified access level."""
        self.user_levels[user_id] = level

    def set_document_level(self, doc_id: str, level: int) -> None:
        """Set the required access level for a document."""
        self.document_levels[doc_id] = level

    def can_access_document(self, user_id: str, doc_id: str) -> bool:
        """Check if the user can access a document based on their access level."""
        if doc_id not in self.document_levels:
            return False
        user_level = self.user_levels.get(user_id, 0)
        required_level = self.document_levels[doc_id]
        return user_level >= required_level