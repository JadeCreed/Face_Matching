from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    middle_initial = models.CharField(max_length=10, blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    year_section = models.CharField(max_length=50, blank=True, null=True)

    # Photo uploaded from student form (left side)
    form_photo = models.ImageField(upload_to='form_photos/', blank=True, null=True)

    # Photo saved in student list (right side)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    e_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        default='no',  # 'completed', 'not_yet', 'no'
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
