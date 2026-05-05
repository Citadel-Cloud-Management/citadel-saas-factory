"""Celery application — async task queue for background jobs."""

import os

from celery import Celery

broker_url = os.environ.get("RABBITMQ_URL", "amqp://citadel:citadel@localhost:5672")
result_backend = os.environ.get("REDIS_URL", "redis://localhost:6379/1")

celery_app = Celery(
    "citadel",
    broker=broker_url,
    backend=result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_queue="default",
    task_queues={
        "default": {"exchange": "default", "routing_key": "default"},
        "email": {"exchange": "email", "routing_key": "email"},
        "compliance": {"exchange": "compliance", "routing_key": "compliance"},
        "webhooks": {"exchange": "webhooks", "routing_key": "webhooks"},
    },
    beat_schedule={
        "check-kyc-expirations": {
            "task": "app.workers.tasks.check_kyc_expirations",
            "schedule": 3600.0,  # Every hour
        },
        "compliance-daily-report": {
            "task": "app.workers.tasks.generate_compliance_report",
            "schedule": 86400.0,  # Daily
        },
        "cleanup-expired-sessions": {
            "task": "app.workers.tasks.cleanup_expired_sessions",
            "schedule": 7200.0,  # Every 2 hours
        },
    },
)

celery_app.autodiscover_tasks(["app.workers"])
