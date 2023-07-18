from django.db import models

from users.models import User


class Notification(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    body = models.TextField()
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        ordering = ('-id',)

    def __str__(self):

        return self.title