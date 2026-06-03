import pytest

from main import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str_and_repr():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"
    assert repr(ingredient) == "Ingredient('Мука', 500.0, 'г')"


def test_ingredient_equal():
    first = Ingredient("Мука", 500, "г")
    second = Ingredient("Мука", 300, "г")

    assert first == second


def test_ingredient_not_equal():
    flour = Ingredient("Мука", 500, "г")
    sugar = Ingredient("Сахар", 500, "г")
    flour_kg = Ingredient("Мука", 1, "кг")

    assert flour != sugar
    assert flour != flour_kg


def test_ingredient_bad_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -100, "г")


def test_recipe_creation():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    assert recipe.title == "Пицца"
    assert recipe.ingredients == [flour]


def test_recipe_add_new_ingredient():
    recipe = Recipe("Пицца")
    flour = Ingredient("Мука", 500, "г")
    recipe.add_ingredient(flour)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"


def test_recipe_add_same_ingredient():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_scale():
    recipe = Recipe("Пицца", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сыр", 200, "г")
    ])
    new_recipe = recipe.scale(2)

    assert new_recipe is not recipe
    assert new_recipe.title == "Пицца"
    assert new_recipe.ingredients[0].quantity == 1000.0
    assert new_recipe.ingredients[1].quantity == 400.0
    assert recipe.ingredients[0].quantity == 500.0


def test_recipe_scale_bad_ratio():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))

    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сыр", 200, "г")
    ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()

    assert len(result) == 2
    assert result[0].quantity == 1000.0
    assert result[1].quantity == 400.0


def test_shopping_list_bad_portions():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    cake = Recipe("Кекс", [Ingredient("Сахар", 100, "г")])
    shopping_list = ShoppingList()

    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(cake, 1)
    shopping_list.remove_recipe("Пицца")
    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Сахар"


def test_shopping_list_get_list():
    pizza = Recipe("Пицца", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сыр", 200, "г")
    ])
    cake = Recipe("Кекс", [
        Ingredient("Мука", 300, "г"),
        Ingredient("Сахар", 100, "г")
    ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(cake, 1)
    result = shopping_list.get_list()
    names = []

    for ingredient in result:
        names.append(ingredient.name)

    assert len(result) == 3
    assert names == ["Мука", "Сахар", "Сыр"]
    assert result[0].quantity == 800.0


def test_shopping_list_add():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    cake = Recipe("Кекс", [Ingredient("Сахар", 100, "г")])

    first_list = ShoppingList()
    second_list = ShoppingList()

    first_list.add_recipe(pizza, 1)
    second_list.add_recipe(cake, 1)

    new_list = first_list + second_list

    assert len(new_list.get_list()) == 2
    assert len(first_list.get_list()) == 1
    assert len(second_list.get_list()) == 1


def test_dietary_recipe_scale():
    recipe = DietaryRecipe("Пицца", "веган", [
        Ingredient("Мука", 500, "г")
    ])
    new_recipe = recipe.scale(2)

    assert isinstance(new_recipe, DietaryRecipe)
    assert new_recipe.diet_type == "веган"
    assert new_recipe.ingredients[0].quantity == 1000.0


def test_dietary_recipe_str():
    recipe = DietaryRecipe("Пицца", "веган", [
        Ingredient("Мука", 500, "г")
    ])
    text = str(recipe)

    assert text.startswith("[веган]")
    assert "Пицца" in text
