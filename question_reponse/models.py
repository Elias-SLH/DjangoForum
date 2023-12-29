from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Question(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    topic = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    upvote = models.ManyToManyField(User, related_name='question_upvote')
    downvote = models.ManyToManyField(User, related_name='question_downvote')

    def __str__(self):
        return f'[{self.id}] {self.topic} by {self.user}'

    def total_upvote(self):
        return self.upvote.count()

    def get_absolute_url(self):
        return reverse('qr:detail', kwargs={'pk': self.pk})


class Answer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, related_name="quest", null=True, on_delete=models.CASCADE)
    reply = models.TextField(null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Answer ({self.id}) for question [{self.question.id}]  by {self.user}'

    def get_absolute_url(self):
        return reverse('qr:detail', kwargs={'pk': self.question.pk})
