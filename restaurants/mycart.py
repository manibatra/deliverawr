from carton.cart import CartItem
from carton.cart import Cart
import json

from decimal import Decimal

from carton import settings as carton_settings
from .models import MenuItem



class ModifiedCartItem(CartItem):
	def __init__(self, product, quantity, price, add_ons, removed, item_no):
		super(ModifiedCartItem, self).__init__(product, quantity, price)
		self.add_ons = add_ons
		self.removed = removed
		self.item_place = item_no

	def to_dict(self):
		add_on_dict = []
		for add_on in self.add_ons:
			add_on_item = {}
			add_on_item['product_pk'] = add_on.pk
			add_on_item['price'] = str(add_on.price)
			add_on_dict.append(add_on_item)

		removed_dict = []
		for remove in self.removed:
			removed_item = {}
			removed_item['product_pk'] = remove.pk
			removed_item['price'] = str(remove.price)
			removed_dict.append(removed_item)

		return {
			'product_pk': self.product.pk,
			'quantity': self.quantity,
			'price': str(self.price),
			'add_ons' : json.dumps(add_on_dict),
			'removed' : json.dumps(removed_dict),
			'item_no' : self.item_place,
            'subtotal' : str(self.subtotal)
		}

	@property
	def subtotal(self):
		'''
		Subtotal for cart items including add-ons
		'''
		add_on_charges = 0
		for add_on in self.add_ons:
			add_on_charges += add_on.price

		total_product_charge = (self.price * self.quantity) + add_on_charges

		return total_product_charge




class ModifiedCart(Cart):

    """
    A cart that lives in the session.
    """
    def __init__(self, session, session_key=None):
        self._items_dict = {}
        self.session = session
        self.session_key = session_key or carton_settings.CART_SESSION_KEY
        self.item_no = 0
            # If a cart representation was previously stored in session, then we
        if self.session_key in self.session:
            # rebuild the cart object from that serialized representation.
            cart_representation = self.session[self.session_key]
            cart_product_keys = cart_representation.keys()
            ids_in_cart = []
            for key in cart_product_keys:
            	product = MenuItem.objects.get(pk = cart_representation[key]['product_pk'])
            	add_ons = []
            	removed = []
            	add_on_list = json.loads(cart_representation[key]['add_ons'])
            	removed_list = json.loads(cart_representation[key]['removed'])

            	for add_on in add_on_list:
            		add_on_item = MenuItem.objects.get(pk = add_on['product_pk'])
            		add_ons.append(add_on_item)

            	for remove in removed_list:
            		removed_item = MenuItem.objects.get(pk = remove['product_pk'])
            		removed.append(removed_item)


            	self._items_dict[self.item_no] = ModifiedCartItem(product, cart_representation[key]['quantity'],
            									Decimal(cart_representation[key]['price']), add_ons, removed, self.item_no)
            	self.item_no += 1



    def __contains__(self, product):
        """
        Checks if the given product is in the cart.
        """
        return product in self.products

    def get_product_model(self):
        return module_loading.get_product_model()


    def get_queryset(self):
        product_model = self.get_product_model()
        queryset = product_model._default_manager.all()
        queryset = self.filter_products(queryset)
        return queryset

    def update_session(self):
        """
        Serializes the cart data, saves it to session and marks session as modified.
        """
        self.session[self.session_key] = self.cart_serializable
        self.session.modified = True

    def add(self, product, add_ons, removed, price=None, quantity=1):
        """
        Adds or creates products in cart. For an existing product,
        the quantity is increased and the price is ignored.
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')

        if price == None:
            raise ValueError('Missing price when adding to cart')
        self._items_dict[self.item_no] = ModifiedCartItem(product, quantity, price, add_ons, removed, self.item_no)
        self.item_no += 1
        self.update_session()

    def remove(self, item_id):
        """
        Removes the product.
        """
        if item_id in self._items_dict.keys():
            del self._items_dict[item_id]
            self.update_session()

    def remove_single(self, product):
        """
        Removes a single product by decreasing the quantity.
        """
        if product in self.products:
            if self._items_dict[product.pk].quantity <= 1:
                # There's only 1 product left so we drop it
                del self._items_dict[product.pk]
            else:
                self._items_dict[product.pk].quantity -= 1
            self.update_session()

    def clear(self):
        """
        Removes all items.
        """
        self._items_dict = {}
        self.update_session()

    def set_quantity(self, product, quantity):
        """
        Sets the product's quantity.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError('Quantity must be positive when updating cart')
        if product in self.products:
            self._items_dict[product.pk].quantity = quantity
            if self._items_dict[product.pk].quantity < 1:
                del self._items_dict[product.pk]
            self.update_session()

    @property
    def items(self):
        """
        The list of cart items.
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        The serializable representation of the cart.
        For instance:
        {
            '1': {'product_pk': 1, 'quantity': 2, price: '9.99', add_ons: [{'product_pk' : 3, 'price' : 1.5}, {'product_pk' : 4, 'price' : 2.99}]},
        }
        Note how the product pk servers as the dictionary key.
        """
        cart_representation = {}
        item_no = 0
        for item in self.items:
            # JSON serialization: object attribute should be a string
            product_id = str(item_no)
            item_no += 1
            cart_representation[product_id] = item.to_dict()
        return cart_representation


    @property
    def items_serializable(self):
        """
        The list of items formatted for serialization.
        """
        return self.cart_serializable.items()

    @property
    def count(self):
        """
        The number of items in cart, that's the sum of quantities.
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        return len(self._items_dict)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def products(self):
        """
        The list of associated products numbers i.e. item ids.
        """
        return [item.item_place for item in self.items]

    @property
    def total(self):
        """
        The total value of all items in the cart.
        """
        return sum([item.subtotal for item in self.items])

