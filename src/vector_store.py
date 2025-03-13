from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document
from access_control import AccessControl

class VectorStore:
    def __init__(self, access_control: Optional[AccessControl] = None):
        self.embeddings = OllamaEmbeddings(model="llama2")
        self.vector_store = None
        self.access_control = access_control

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4, user_id: str = None) -> List[Document]:
        """Search for similar documents and apply access control filtering if a user_id is provided."""
        if self.vector_store is None:
            return []
        results = self.vector_store.similarity_search(query, k=k)
        if user_id and self.access_control:
            filtered_results = []
            for doc in results:
                doc_id = doc.metadata.get("doc_id")
                if doc_id and self.access_control.can_access_document(user_id, doc_id):
                    filtered_results.append(doc)
            return filtered_results
        return results