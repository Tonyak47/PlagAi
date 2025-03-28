from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField

def user_directory_path(instance, filename):
    """Upload profile images to media/profile_pics/{username}/"""
    return f'profile_pics/{instance.user.username}/{filename}'

class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = [
        ('text', 'Text'),
        ('code', 'Code'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPE_CHOICES)
    content = models.TextField()
    similarity_score = models.FloatField(null=True, blank=True)
<<<<<<< HEAD
    report = models.TextField(null=True, blank=True)
=======
    matched_content = models.TextField(null=True, blank=True)  # Store the matched reference text or code
>>>>>>> e1dc1b7 (Initial commit)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.submission_type} submission on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default="default.png",
        blank=True,
        null=True
    )
    cropping = ImageRatioField('profile_picture', '300x300')

    def __str__(self):
<<<<<<< HEAD
        return self.user.username
=======
        return self.user.username


class Reference(models.Model):
    REFERENCE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('code', 'Code'),
    ]
    reference_type = models.CharField(max_length=10, choices=REFERENCE_TYPE_CHOICES)
    content = models.TextField(unique=True)  # Avoid duplicate references
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference_type} Reference - {self.id}"
>>>>>>> e1dc1b7 (Initial commit)
