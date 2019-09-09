from django.db import models


class Todo(models.Model):
    name = models.CharField('NAME', max_length=5, blank=True)
    todo = models.CharField('TODO', max_length=50)

    def __str__(self):
        return self.todo

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.name: # name에 값이 없다면
            self.name = '홍길동' # name에 홍길동을 넣고 저장하라
        super().save()