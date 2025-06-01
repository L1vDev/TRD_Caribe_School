from django.db import models

class SaleStatistics(models.Model):
    date=models.DateField()
    amount=models.DecimalField(default=0,max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.date}: {self.amount}"