from django.db import models
from django.contrib.auth.models import User

class IdeaHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.TextField()
    vibe = models.CharField(
        max_length=20, choices=[("Professional", "Professional"), ("Fun", "Fun")]
    )
    output = models.TextField()  # Stores the full AI response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.idea[:30]}"