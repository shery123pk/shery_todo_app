"""
Event Streaming with Kafka
Phase V: Advanced Cloud Deployment
Author: Sharmeen Asif
"""

from typing import Optional
import json
import os


try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False


class EventProducer:
    """Kafka event producer for task events"""

    def __init__(self):
        """Initialize Kafka producer if available"""
        self.enabled = os.getenv("KAFKA_ENABLED", "false").lower() == "true"
        self.producer: Optional[KafkaProducer] = None

        if self.enabled and KAFKA_AVAILABLE:
            kafka_brokers = os.getenv("KAFKA_BROKERS", "kafka-service:9092")
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=kafka_brokers.split(","),
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Kafka producer: {e}")
                self.enabled = False

    async def send_event(self, topic: str, event: dict):
        """
        Send event to Kafka topic.

        Args:
            topic: Kafka topic name
            event: Event data dictionary
        """
        if not self.enabled or not self.producer:
            return

        try:
            self.producer.send(topic, value=event)
            self.producer.flush()
        except Exception as e:
            print(f"Error sending event to Kafka: {e}")

    async def task_created(self, task_data: dict):
        """Send task.created event"""
        await self.send_event("task.created", {
            "event_type": "task.created",
            "task_id": str(task_data["id"]),
            "user_id": str(task_data["user_id"]),
            "title": task_data["title"],
            "timestamp": task_data["created_at"].isoformat()
        })

    async def task_updated(self, task_id: str, user_id: str, changes: dict):
        """Send task.updated event"""
        await self.send_event("task.updated", {
            "event_type": "task.updated",
            "task_id": task_id,
            "user_id": user_id,
            "changes": changes,
            "timestamp": None
        })

    async def task_deleted(self, task_id: str, user_id: str):
        """Send task.deleted event"""
        await self.send_event("task.deleted", {
            "event_type": "task.deleted",
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": None
        })

    async def task_completed(self, task_id: str, user_id: str, completed: bool):
        """Send task.completed event"""
        await self.send_event("task.completed", {
            "event_type": "task.completed",
            "task_id": task_id,
            "user_id": user_id,
            "completed": completed,
            "timestamp": None
        })


# Global event producer instance
event_producer = EventProducer()
