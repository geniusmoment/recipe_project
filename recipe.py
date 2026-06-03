class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, new_quantity):
        if new_quantity > 0:
            self._quantity = float(new_quantity)
        else:
            raise ValueError("Количество должно быть положительным")
        
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name and self.unit == other.unit
        
class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = []
        if ingredients is not None:
            for i in ingredients:
                self.add_ingredient(i)

    def add_ingredient(self, ingredient: Ingredient):
        if ingredient in self.ingredients:
            ind = self.ingredients.index(ingredient)
            self.ingredients[ind].quantity += ingredient.quantity
        else:
            self.ingredients.append(Ingredient(ingredient.name, ingredient.quantity, ingredient.unit))

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)):
            return ratio > 0
        return False
        
    def scale(self, ratio: float):
        if not self.is_valid_ratio:
            raise ValueError('множитель должен быть положительным')
        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredients.append(Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit))
        return Recipe(self.title, new_ingredients)
    
    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        return f"{self.title}: {', '.join(str(i) for i in self.ingredients)}"
    
class ShoppingList:
    def __init__(self):
        self.items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_portions = recipe.scale(portions)
        for i in scaled_portions.ingredients:
            self.items.append((i, scaled_portions.title))


    def remove_recipe(self, title: str):
        new_items = []
        for i, t in self.items:
            if t != title:
                new_items.append((i, t))
        self.items = new_items

    def get_list(self):
        ingredients_dict = {}
        for i, t in self.items:
            key = (i.name, i.unit)
            if key in ingredients_dict:
                ingredients_dict[key] += i.quantity
            else:
                ingredients_dict[key] = i.quantity
        ans = []
        for (name, unit), quantity in ingredients_dict.items():
            ans.append(Ingredient(name, quantity, unit))
        ans.sort(key = lambda x: x.name)
        return ans
    
    def __add__(self, other):
        if isinstance(other, ShoppingList):
            new_list = ShoppingList()
            new_list.items = self.items + other.items
            return new_list
        
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        new_ingredients = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, new_ingredients)
    
    def __str__(self):
        ans = super().__str__()
        return f"[{self.diet_type}] {ans}"