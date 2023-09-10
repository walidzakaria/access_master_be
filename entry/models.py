from django.db import models

# Create your models here.
class QrCode(models.Model):
    qr_code = models.CharField(max_length=20, unique=True, db_index=True)

    def __str__(self):
        return self.qr_code


class Entry(models.Model):
    qr_code = models.OneToOneField(QrCode, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qr_code.qr_code
    
    class Meta:
        verbose_name_plural = 'Entries'