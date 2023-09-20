from django.db import models

# Create your models here.
class Branch(models.Model):
    branch = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.branch
    
    class Meta:
        verbose_name_plural = 'Branches'

class PrintOrder(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.id}'


class QrCode(models.Model):
    print_order = models.ForeignKey(PrintOrder, on_delete=models.CASCADE, db_index=True)
    qr_code = models.CharField(max_length=20, unique=True, db_index=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.qr_code


class Entry(models.Model):
    qr_code = models.OneToOneField(QrCode, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.qr_code.qr_code
    
    class Meta:
        verbose_name_plural = 'Entries'