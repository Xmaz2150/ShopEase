from models.models import Category

'''TEMPORARY'''
categories = ['Clothing', 'Shoes', 'Electronics', 'Books', 'Games', 'Beauty_Health', 'Food_And_Beverage', 'Hand_Bags', 'Jewellery_And_Accessories', 'Home_And_Gifts']
def add_category(name):
    """Add a new category to the database"""
    print("Adding category: ", name)
    if not name:
        raise ValueError("Category name cannot be empty")
    
    new_category = Category(name=name)
    new_category.save()
    return new_category

def init_categories():
    for c in categories:
        add_category(c)