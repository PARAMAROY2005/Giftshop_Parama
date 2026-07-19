from django.db import models

class Gift(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

    def __str__(self):
        return self.gift.name


class Cart(models.Model):

    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.gift.name