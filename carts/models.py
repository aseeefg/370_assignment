from django.db import models
from store.models import Product
from accounts.models import Account # Import your custom account model

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True) # Added this
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True) # Set null=True
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    # Fixed: return self.product.product_name (or whatever field stores the name)
    def __str__(self):
        return str(self.product)