"""
Qdrant Vector Database Service
Provides semantic search for tasks using embeddings
Author: Sharmeen Asif
"""

import os
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import hashlib


class QdrantService:
    """Service for managing task embeddings in Qdrant vector database"""

    def __init__(self):
        """Initialize Qdrant client and OpenAI for embeddings"""
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION", "todo_embeddings")

        if not qdrant_url:
            print("⚠️ QDRANT_URL not configured. Semantic search disabled.")
            self.client = None
            self.openai_client = None
            return

        try:
            # Initialize Qdrant client
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key if qdrant_api_key else None,
            )

            # Initialize OpenAI for embeddings
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key:
                self.openai_client = OpenAI(api_key=openai_api_key)
            else:
                print("⚠️ OPENAI_API_KEY not configured. Using Qdrant without embeddings.")
                self.openai_client = None

            # Ensure collection exists
            self._ensure_collection()

            print("✅ Qdrant service initialized successfully")
        except Exception as e:
            print(f"⚠️ Failed to initialize Qdrant: {e}")
            self.client = None
            self.openai_client = None

    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        if not self.client:
            return

        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)

            if not exists:
                # Create collection with 1536 dimensions (OpenAI ada-002 embedding size)
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                print(f"✅ Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            print(f"⚠️ Error ensuring collection: {e}")

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding vector for text using OpenAI.

        Args:
            text: The text to embed

        Returns:
            List of floats representing the embedding, or None if failed
        """
        if not self.openai_client:
            return None

        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ Error getting embedding: {e}")
            return None

    def _generate_point_id(self, task_id: str) -> str:
        """
        Generate a deterministic point ID from task ID.

        Args:
            task_id: The task UUID

        Returns:
            A hash of the task ID as a string
        """
        return hashlib.md5(task_id.encode()).hexdigest()

    async def index_task(self, task_id: str, title: str, description: Optional[str] = None):
        """
        Index a task in Qdrant for semantic search.

        Args:
            task_id: The task UUID
            title: Task title
            description: Task description (optional)
        """
        if not self.client or not self.openai_client:
            return

        try:
            # Combine title and description for embedding
            text = title
            if description:
                text += f"\n{description}"

            # Get embedding
            embedding = self._get_embedding(text)
            if not embedding:
                return

            # Create point
            point_id = self._generate_point_id(task_id)
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "task_id": task_id,
                    "title": title,
                    "description": description or "",
                }
            )

            # Upsert to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        except Exception as e:
            print(f"⚠️ Error indexing task: {e}")

    async def search_tasks(self, query: str, limit: int = 10) -> List[str]:
        """
        Search for tasks using semantic similarity.

        Args:
            query: The search query
            limit: Maximum number of results

        Returns:
            List of task IDs matching the query
        """
        if not self.client or not self.openai_client:
            return []

        try:
            # Get query embedding
            embedding = self._get_embedding(query)
            if not embedding:
                return []

            # Search in Qdrant
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                limit=limit,
            )

            # Extract task IDs
            return [r.payload.get("task_id") for r in results if r.payload]
        except Exception as e:
            print(f"⚠️ Error searching tasks: {e}")
            return []

    async def delete_task(self, task_id: str):
        """
        Delete a task from Qdrant index.

        Args:
            task_id: The task UUID to delete
        """
        if not self.client:
            return

        try:
            point_id = self._generate_point_id(task_id)
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id]
            )
        except Exception as e:
            print(f"⚠️ Error deleting task from Qdrant: {e}")


# Global Qdrant service instance
qdrant_service = QdrantService()
