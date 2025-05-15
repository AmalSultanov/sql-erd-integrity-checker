from django.contrib.auth.models import User
from django.db import models


class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submission #{self.pk} - {self.status} by {self.user.pk}'

    class Meta:
        verbose_name = 'submission'
        verbose_name_plural = 'submissions'


class AILogEntryModel(models.Model):
    model_version = models.CharField(max_length=15)
    is_response = models.BooleanField()
    res_text = models.JSONField()
    is_request = models.BooleanField()
    req_prompt = models.TextField()
    req_token_length = models.PositiveIntegerField()
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'AILogEntry - {'Response' if self.is_response else 'Request'}'

    class Meta:
        verbose_name = 'AI log entry'
        verbose_name_plural = 'AI log entries'


class NotationMapping(models.Model):
    symbol = models.CharField(max_length=100, unique=True)
    modality = models.CharField(max_length=10)
    side = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.symbol} ({self.modality}, {self.side})'

    class Meta:
        verbose_name = 'notation'
        verbose_name_plural = 'notations'


class KnowledgeBase(models.Model):
    first_entity = models.CharField(max_length=20)
    second_entity = models.CharField(max_length=20)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    first_modality = models.CharField(max_length=10)
    second_modality = models.CharField(max_length=10)
    relationship_name = models.CharField(max_length=20)
    ai_log_entry = models.OneToOneField(
        AILogEntryModel, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.first_entity} ({self.first_modality}) - '
            f'{self.relationship_name} - '
            f'{self.second_entity} ({self.second_modality})'
        )

    class Meta:
        verbose_name = 'knowledge base'
        verbose_name_plural = 'knowledge bases'
        constraints = [
            models.UniqueConstraint(
                fields=['first_entity', 'second_entity', 'submission'],
                name='unique_kb_composite_key'
            )
        ]


class MapInto(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    symbol = models.ForeignKey(NotationMapping, on_delete=models.CASCADE)
    first_entity = models.ForeignKey(
        KnowledgeBase, on_delete=models.CASCADE, related_name='first_entities'
    )
    second_entity = models.ForeignKey(
        KnowledgeBase, on_delete=models.CASCADE, related_name='second_entities'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'MapInto #{self.pk} for submission #{self.submission.pk})'

    class Meta:
        verbose_name = 'map into'
        verbose_name_plural = 'map into'
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'symbol', 'first_entity',
                        'second_entity'],
                name='unique_mi_composite_key'
            )
        ]


class MismatchModel(models.Model):
    ai_log_entry = models.ForeignKey(AILogEntryModel, on_delete=models.CASCADE)
    description = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mismatch on log #{self.ai_log_entry.pk} at {self.created_at}'

    class Meta:
        verbose_name = 'mismatch'
        verbose_name_plural = 'mismatches'
        constraints = [
            models.UniqueConstraint(
                fields=['ai_log_entry', 'created_at'],
                name='unique_mismatch_composite_key'
            )
        ]


class ProduceModel(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    mismatch_ai_log_entry = models.ForeignKey(
        MismatchModel,
        on_delete=models.CASCADE,
        related_name='produce_mismatch_ai_log_entries'
    )
    mismatch_created_at = models.ForeignKey(
        MismatchModel,
        on_delete=models.CASCADE,
        related_name='produce_mismatch_created_ats'
    )
    kb_first_entity = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='produce_first_entities'
    )
    kb_second_entity = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='produce_second_entities'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ProduceModel for submission #{self.submission.pk}'

    class Meta:
        verbose_name = 'produce'
        verbose_name_plural = 'produce'
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'mismatch_ai_log_entry',
                        'mismatch_created_at', 'kb_first_entity',
                        'kb_second_entity'],
                name='unique_ai_log_entry_timestamp'
            )
        ]
