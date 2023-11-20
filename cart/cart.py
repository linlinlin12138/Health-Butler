from decimal import Decimal
from django.conf import settings
from healthbutler.models import Foods

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, food, serving=1,override_serving=False):
        food_id = str(food.id)
        if food_id not in self.cart:
            self.cart[food_id] = {'serving': 0,
                                     'calories': str(food.calories)}
        if override_serving:
            self.cart[food_id]['serving'] = serving
        else:
            self.cart[food_id]['serving'] += serving
        self.save()


    def save(self):
        # update the cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # make sure it is saved
        self.session.modified = True

    def remove(self, food):
        #Remove food from the cart.
        food_id = str(food.id)
        if food_id in self.cart:
            del self.cart[food_id]
            self.save()


    def __iter__(self):
        #Iterate over the items in the cart and get the foods from my database.
        food_ids = self.cart.keys()
        # get the food objects and add them to the cart
        foods = Foods.objects.filter(id__in=food_ids)
        for food in foods:
            self.cart[str(food.id)]['food'] = food

        for item in self.cart.values():
            item['calories'] = Decimal(item['calories'])
            item['total_calories'] = item['calories'] * item['serving']
            yield item

    def __len__(self):
        #Count all items in the cart.
        return sum(item['serving'] for item in self.cart.values())

    def get_total_calories(self):
        return sum(Decimal(item['calories']) * item['serving'] for item in self.cart.values())

def clear(self):
    # clear cart
    del self.session[settings.CART_SESSION_ID]
    self.session.modified = True

