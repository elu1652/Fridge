class Ingredient:
    def __init__(self, name, quantity, unit, expiry_date=None):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.expiry_date = expiry_date  