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


class ShoppingList:

    def __init__(self):
        self._items = []


    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))


    def remove_recipe(self, title: str):
        new_items = []
        for ingredient, recipe_name in self._items:
            if recipe_name != title:
                new_items.append((ingredient, recipe_name))
        self._items = new_items


    def get_list(self):
        products = {}

        for ingredient, recipe_name in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in products:
                products[key] += ingredient.quantity
            else:
                products[key] = ingredient.quantity

        answer = []
        for key in products:
            name = key[0]
            unit = key[1]
            quantity = products[key]
            answer.append(Ingredient(name, quantity, unit))
        answer.sort(key=lambda ingredient: ingredient.name)

        return answer


    def __add__(self, other):
        result = ShoppingList()
        for item in self._items:
            result._items.append(item)
        for item in other._items:
            result._items.append(item)
        return result


class DietaryRecipe(Recipe):

    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type


    def scale(self, ratio):
        scaled = super().scale(ratio)
        return DietaryRecipe(
            self.title,
            self.diet_type,
            scaled.ingredients
        )


    def __str__(self):
        return f"[{self.diet_type}] " + super().__str__()
