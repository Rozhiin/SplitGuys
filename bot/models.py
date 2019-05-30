from django.db import models


# Create your models here.
class Costs(models.Model):
    name = models.CharField(default=None, max_length=100)
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    payer_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    amount = models.IntegerField(default=0, max_length=20)
    payment_id = models.CharField(default=None, max_length=20)
    description = models.CharField(default=None, max_length=100)


class Owe(models.Model):
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    creditor_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    debtor_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    amount = models.IntegerFiaeld(default=0, max_length=20)



class Shares(models.Model):
    payment_id = models.CharField(default=None, max_length=20)
    user_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    share = models.FloatField(default=0.0, max_length=5)
