class Ingredient:

    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value


    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"


    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"


    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit


class Recipe:

    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients


    def add_ingredient(self, ingredient):
        for old_ingredient in self.ingredients:
            if old_ingredient == ingredient:
                old_ingredient.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)


    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio) == int or type(ratio) == float:
            return ratio > 0
        return False


    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")

        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity * ratio,
                ingredient.unit
            )
            new_ingredients.append(new_ingredient)
        return Recipe(self.title, new_ingredients)


    def __len__(self):
        return len(self.ingredients)


    def __str__(self):
        text = self.title + "\n"
        for ingredient in self.ingredients:
            text += str(ingredient) + "\n"
        return text
