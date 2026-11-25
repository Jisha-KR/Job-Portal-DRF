from django.db import models
from accounts.models import User

class Job(models.Model):
    title = models.CharField(max_length=100)  # e.g. Python Developer
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # Kochi, Trivandrum, Remote
    salary = models.CharField(max_length=50, blank=True)  # e.g. 25000-35000
    description = models.TextField()
    skills_required = models.CharField(max_length=200)  # Python, Django, React
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # One person can't apply twice to same job

    def __str__(self):
        return f"{self.applicant.email} -> {self.job.title}"