from django.db import models


# Create your models here.
class Cost(models.Model):
    name = models.CharField(default=None, max_length=100)
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    payer_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    amount = models.IntegerField(default=0)
    payment_id = models.CharField(default=None, max_length=20)
    description = models.CharField(default=None, max_length=100)


class Owe(models.Model):
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    creditor_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    debtor_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    amount = models.IntegerField(default=0)


class Share(models.Model):
    payment_id = models.CharField(default=None, max_length=20)
    user_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    share = models.FloatField(default=0.0, max_length=5)


class State(models.Model):
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    user_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    last_command = models.IntegerField(default=0)
    command_state = models.IntegerField(default=0)


class Cache(models.Model):
    group_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    user_id = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    var_name = models.CharField(default=None, max_length=100)  # TODO: 1.check max_length 2.set default
    value = models.FloatField(default=0)
