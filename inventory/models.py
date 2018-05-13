from django.db import models


class Item(models.Model):
    internal_id = models.CharField(max_length=20)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    vendor = models.CharField(max_length=250, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qty_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=-1)
    qty_in_reorder = models.IntegerField(default=0)
    t_code = models.CharField(max_length=200, null=True, blank=True)

    @property
    def inventory_value(self):
        return '$%.2f' % (self.unit_price*self.qty_in_stock)

    @property
    def unit_price_dollars(self):
        return '$%.2f' % self.unit_price

    def __str__(self):
        return '%s - %s' % (self.internal_id, self.name)
