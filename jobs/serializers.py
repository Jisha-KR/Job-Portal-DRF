from rest_framework import serializers
from .models import Job, Application

class JobSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.ReadOnlyField(source='posted_by.full_name')
    posted_by_email = serializers.ReadOnlyField(source='posted_by.email')

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'salary', 'description', 'skills_required', 'posted_by', 'posted_by_name', 'posted_by_email', 'created_at', 'is_active']
        read_only_fields = ['posted_by', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    applicant_name = serializers.ReadOnlyField(source='applicant.full_name')

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applicant', 'applicant_name', 'resume_link', 'cover_letter', 'status', 'applied_at']
        read_only_fields = ['applicant', 'applied_at', 'status']