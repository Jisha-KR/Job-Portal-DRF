from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'company', 'location', 'skills_required', 'description']

    def get_permissions(self):
        # Anyone can see jobs, only logged-in can post/apply
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Only recruiter can post job
        if self.request.user.user_type != 'recruiter':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only Recruiter can post jobs")
        serializer.save(posted_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        job = self.get_object()
        # Only seeker can apply
        if request.user.user_type != 'seeker':
            return Response({"error": "Only Job Seekers can apply"}, status=status.HTTP_403_FORBIDDEN)
        # Already applied?
        if Application.objects.filter(job=job, applicant=request.user).exists():
            return Response({"error": "You already applied to this job"}, status=status.HTTP_400_BAD_REQUEST)

        app = Application.objects.create(
            job=job,
            applicant=request.user,
            resume_link=request.data.get('resume_link', ''),
            cover_letter=request.data.get('cover_letter', '')
        )
        return Response(ApplicationSerializer(app).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        # Recruiter: jobs I posted
        jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
        return Response(JobSerializer(jobs, many=True).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_applications(self, request):
        # Seeker: jobs I applied to
        apps = Application.objects.filter(applicant=request.user).order_by('-applied_at')
        return Response(ApplicationSerializer(apps, many=True).data)