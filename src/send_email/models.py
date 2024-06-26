from django.db import models

class MailingListMember(models.Model):
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    body = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
