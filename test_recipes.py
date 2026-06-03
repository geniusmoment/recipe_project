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

class TestRecipe:

    def test_recipe_creation(self):
        ingredient_a = Ingredient("Бананы", 3, "кг")
        ingredient_b = Ingredient("Молоко", 1, "кг")
        recipe = Recipe("Коктейль", [ingredient_a, ingredient_b])
        assert recipe.title == 'Коктейль'
        assert len(recipe) == 2
        assert recipe.ingredients[0].name == 'Бананы'

    def test_add_ingredient_new(self):
        recipe = Recipe("Коктейль")
        new_ingredient = Ingredient("Клубника", 100, "г")
        recipe.add_ingredient(new_ingredient)
        actual = len(recipe.ingredients)
        expected = 1
        assert actual == expected
        assert recipe.ingredients[0].name == "Клубника"
        assert recipe.ingredients[0].quantity == 100.0

    def test_add_ingredient_duplicate(self):
        ingredient_a = Ingredient("Мясо", 2, "кг")
        ingredient_b = Ingredient("Мясо", 3, "кг")
        recipe = Recipe("Шашлык", [ingredient_a])
        recipe.add_ingredient(ingredient_b)
        actual = len(recipe.ingredients)
        expected = 1
        assert actual == expected
        actual_2 = recipe.ingredients[0].quantity
        expected_2 = 5.0
        assert actual_2 == expected_2

    def test_scale(self):
        ingredient_a = Ingredient("Пиво", 999, "мл")
        ingredient_b = Ingredient("Водка", 500, "мл")
        original_recipe = Recipe("Хороший вечер", [ingredient_a, ingredient_b])
        ratio = 2.0
        scaled_recipe = original_recipe.scale(ratio)
        assert scaled_recipe is not original_recipe
        assert scaled_recipe.ingredients[0].quantity == 1998.0 
        assert scaled_recipe.ingredients[1].quantity == 1000.0
        assert scaled_recipe.title == original_recipe.title

    def test_invalid_scale(self):
        ingredient = Ingredient("Порошок", 200, "г")
        recipe = Recipe("Какао", [ingredient])
        invalid_ratio = -2.0
        with pytest.raises(ValueError):
            recipe.scale(invalid_ratio)
    
    def test_len(self):
        ingredient_a = Ingredient("Горох", 200, "г")
        ingredient_b = Ingredient("Бобы", 150, "г")
        ingredient_c = Ingredient("Горох", 50, "г")
        recipe = Recipe("Бобовый горох", [ingredient_a, ingredient_b, ingredient_c])
        actual = len(recipe)
        expected = 2
        assert actual == expected