import uuid
from django.db import models


class VisitorSession(models.Model):
    DEVICE_CHOICES = [
        ("desktop", "Desktop"),
        ("mobile", "Mobile"),
        ("tablet", "Tablet"),
        ("unknown", "Unknown"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.UUIDField(unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    device_type = models.CharField(
        max_length=20, choices=DEVICE_CHOICES, default="unknown"
    )
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    utm_source = models.CharField(max_length=255, null=True, blank=True)
    utm_medium = models.CharField(max_length=255, null=True, blank=True)
    utm_campaign = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Visitor Session"
        verbose_name_plural = "Visitor Sessions"

    def __str__(self):
        return f"Session {self.session_id}"


class PageView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VisitorSession,
        on_delete=models.CASCADE,
        related_name="page_views",
    )
    url = models.TextField()
    title = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"
        indexes = [models.Index(fields=["session", "-created_at"])]

    def __str__(self):
        return f"{self.session.session_id} - {self.url}"


class QuestionInteraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VisitorSession,
        on_delete=models.CASCADE,
        related_name="question_interactions",
    )
    question_id = models.CharField(max_length=100, db_index=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    time_spent_seconds = models.FloatField(default=0.0)
    revisit_count = models.IntegerField(default=0)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Question Interaction"
        verbose_name_plural = "Question Interactions"
        indexes = [
            models.Index(fields=["session", "question_id"]),
            models.Index(fields=["session", "-created_at"]),
        ]
        unique_together = [["session", "question_id", "order_index"]]

    def __str__(self):
        return f"{self.session.session_id} - Q{self.question_id} ({self.order_index})"


class TrackingEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ("pageview", "Pageview"),
        ("cta_click", "CTA Click"),
        ("form_submit", "Form Submit"),
        ("form_abandon", "Form Abandon"),
        ("custom", "Custom"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VisitorSession,
        on_delete=models.CASCADE,
        related_name="tracking_events",
        null=True,
        blank=True,
    )
    event_type = models.CharField(
        max_length=30, choices=EVENT_TYPE_CHOICES, db_index=True
    )
    page_url = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tracking Event"
        verbose_name_plural = "Tracking Events"
        indexes = [
            models.Index(fields=["session", "event_type"]),
            models.Index(fields=["event_type", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.page_url}"