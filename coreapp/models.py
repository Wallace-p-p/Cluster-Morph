from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class Txt(models.Model):
    title = models.CharField(
            max_length=25,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #Txt
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title
