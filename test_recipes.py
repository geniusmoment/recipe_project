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

class TestShoppingList:

    def test_add_recipe(self):
        ingredient = Ingredient("Цыпленок", 1, "шт")
        recipe = Recipe("Ужин", [ingredient])
        shop_list = ShoppingList()
        shop_list.add_recipe(recipe, 2.0)
        answer = shop_list.get_list()
        assert len(answer) == 1
        assert answer[0].name == "Цыпленок"
        assert answer[0].quantity == 2.0

    def test_add_invalid(self):
        ing = Ingredient("Вода", 525252, "мл")
        recipe = Recipe("Чай", [ing])
        shop_list = ShoppingList()
        invalid_portions = -2.0
        with pytest.raises(ValueError):
            shop_list.add_recipe(recipe, portions=invalid_portions)

    def test_remove_recipe(self):
        recipe1 = Recipe("Додо ужин", [Ingredient("Пицца", 5, "шт")])
        recipe2 = Recipe("Тануки ужин", [Ingredient("роллы", 100, "шт")])
        shop_list = ShoppingList()
        shop_list.add_recipe(recipe1, portions=1)
        shop_list.add_recipe(recipe2, portions=1)
        shop_list.remove_recipe("Додо ужин")
        answer = shop_list.get_list()
        assert len(answer) == 1
        assert answer[0].name == "роллы"

    def test_remove_recipe_empty(self):
        recipe = Recipe("Щи", [Ingredient("Капуста", 500, "г")])
        shop_list = ShoppingList()
        shop_list.add_recipe(recipe, portions=1)
        shop_list.remove_recipe("Борщ")
        answer = shop_list.get_list()
        assert len(answer) == 1

    def test_get_list_duplicate(self):
        recipe1 = Recipe("Мохито безалкогольный", [Ingredient("Спрайт", 500, "г"), Ingredient("Мята", 299, "г")])
        recipe2 = Recipe("Май тай", [Ingredient("Ром", 500, "г"), Ingredient("Мята", 300, "г")])
        shop_list = ShoppingList()
        shop_list.add_recipe(recipe1, portions=1)
        shop_list.add_recipe(recipe2, portions=1)
        answer = shop_list.get_list()
        assert len(answer) == 3
        assert answer[0].name == "Мята"
        assert answer[1].name == "Ром"
        assert answer[2].name == "Спрайт"
        assert answer[0].quantity == 599.0

    def test_get_list_unique(self):
        recipe1 = Recipe("Яишница", [Ingredient("Яйца", 5, "шт")])
        recipe2 = Recipe("Каша", [Ingredient("Овсянка", 300, "г")])
        list1 = ShoppingList()
        list1.add_recipe(recipe1, portions=1)
        list2 = ShoppingList()
        list2.add_recipe(recipe2, portions=1)
        combined_list = list1 + list2
        combined_answer = combined_list.get_list()
        assert len(combined_answer) == 2
        assert len(list1.get_list()) == 1
        assert len(list2.get_list()) == 1
        assert combined_list is not list1
        assert combined_list is not list2