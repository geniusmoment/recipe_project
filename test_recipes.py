import pytest
from recipe import Ingredient, Recipe, ShoppingList, DietaryRecipe

class TestIngredient:

    def test_ingredient_creation(self):
        ingredient = Ingredient('Бананы', 3, "кг")
        assert ingredient.name == 'Бананы'
        assert ingredient.quantity == 3
        assert ingredient.unit == 'кг'

    @pytest.mark.parametrize(
        "name, quantity, unit, expected",
        [
            ('Бананы', 3, "кг", "Бананы: 3.0 кг"),
            ("Молоко", 2, "л", "Молоко: 2.0 л"),
            ("Яйца", 2, "шт", "Яйца: 2.0 шт"),
        ]
    )
    def test_str(self, name, quantity, unit, expected):
        ingredient = Ingredient(name, quantity, unit)
        actual = str(ingredient)
        assert actual == expected

    @pytest.mark.parametrize(
        "ingredient_a, ingredient_b, expected",
        [
            (Ingredient("Бананы", 3, "кг"), Ingredient("Бананы", 2, "кг"), True),
            (Ingredient("Бананы", 3, "кг"), Ingredient("Молоко", 1, "кг"), False),
            (Ingredient("Бананы", 3, "кг"), Ingredient("Бананы", 500, "г"), False),
        ]
    )
    def test_eq(self, ingredient_a, ingredient_b, expected):
        actual = (ingredient_b == ingredient_a)
        assert actual == expected