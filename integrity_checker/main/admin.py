from django.contrib import admin

from .models import (
    Submission, AILogEntryModel, NotationMapping, KnowledgeBase, MapInto,
    MismatchModel, ProduceModel
)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']


@admin.register(AILogEntryModel)
class AILogEntryModelAdmin(admin.ModelAdmin):
    list_display = [
        'submission', 'model_version', 'is_response',
        'is_request', 'req_token_length', 'created_at'
    ]
    list_filter = ['model_version', 'is_response', 'is_request', 'created_at']
    search_fields = ['submission__id']


@admin.register(NotationMapping)
class NotationMappingAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'modality', 'side', 'created_at']
    search_fields = ['symbol']
    list_filter = ['modality', 'side', 'created_at']


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = [
        'first_entity', 'second_entity', 'relationship_name',
        'first_modality', 'second_modality', 'submission', 'created_at'
    ]
    search_fields = ['first_entity', 'second_entity', 'relationship_name']
    list_filter = ['first_modality', 'second_modality', 'created_at']


@admin.register(MapInto)
class MapIntoAdmin(admin.ModelAdmin):
    list_display = ['submission', 'symbol', 'first_entity',
                    'second_entity', 'created_at']
    search_fields = ['submission__id', 'symbol__symbol']
    list_filter = ['created_at']


@admin.register(MismatchModel)
class MismatchModelAdmin(admin.ModelAdmin):
    list_display = ['ai_log_entry', 'created_at']
    search_fields = ['ai_log_entry__id']
    list_filter = ['created_at']


@admin.register(ProduceModel)
class ProduceModelAdmin(admin.ModelAdmin):
    list_display = [
        'submission', 'mismatch_ai_log_entry', 'mismatch_created_at',
        'kb_first_entity', 'kb_second_entity', 'created_at'
    ]
    search_fields = ['submission__id']
    list_filter = ['created_at']
