from django.db import models


class Normals(models.IntegerChoices):
    """
    Constants used to represent debits and credits in the database
    """

    DEBIT = 1
    CREDIT = -1
