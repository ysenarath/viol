"""
A data-driven application example using corex.

This example demonstrates how to create a data-driven application that displays
a list of products with filtering and sorting capabilities.
"""
import sys
import os
from typing import List, Dict, Any, Optional

# Add the parent directory to the path so we can import corex
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.corex import (
    Component,
    CorexApp,
    create_app,
    TextComponent,
    ButtonComponent,
    ContainerComponent,
    InputComponent,
    FormComponent,
    CardComponent,
)


# Sample product data
PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop",
        "category": "Electronics",
        "price": 999.99,
        "description": "A powerful laptop with the latest processor and ample storage."
    },
    {
        "id": 2,
        "name": "Smartphone",
        "category": "Electronics",
        "price": 699.99,
        "description": "A feature-rich smartphone with an excellent camera and long battery life."
    },
    {
        "id": 3,
        "name": "Headphones",
        "category": "Electronics",
        "price": 149.99,
        "description": "Noise-cancelling headphones with superior sound quality."
    },
    {
        "id": 4,
        "name": "Coffee Maker",
        "category": "Kitchen",
        "price": 79.99,
        "description": "An automatic coffee maker that brews delicious coffee with the touch of a button."
    },
    {
        "id": 5,
        "name": "Blender",
        "category": "Kitchen",
        "price": 49.99,
        "description": "A high-speed blender perfect for smoothies and soups."
    },
    {
        "id": 6,
        "name": "Desk Chair",
        "category": "Furniture",
        "price": 199.99,
        "description": "An ergonomic desk chair with adjustable height and lumbar support."
    },
    {
        "id": 7,
        "name": "Bookshelf",
        "category": "Furniture",
        "price": 129.99,
        "description": "A sturdy bookshelf with multiple shelves for your books and decorations."
    },
    {
        "id": 8,
        "name": "Table Lamp",
        "category": "Home Decor",
        "price": 39.99,
        "description": "A stylish table lamp that provides warm, ambient lighting."
    }
]


class ProductCard(Component):
    """A component representing a product card."""
    
    def __init__(self, product: Dict[str, Any], id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.product = product
        
        # Create a card component
        card = CardComponent(
            style="""
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            """
        )
        
        # Create product name
        name = TextComponent(
            text=product["name"],
            tag="h3",
            style="margin-top: 0; margin-bottom: 8px;"
        )
        
        # Create product category
        category = TextComponent(
            text=f"Category: {product['category']}",
            style="color: #666; margin-bottom: 8px; font-size: 14px;"
        )
        
        # Create product price
        price = TextComponent(
            text=f"${product['price']:.2f}",
            style="font-weight: bold; color: #4CAF50; margin-bottom: 8px;"
        )
        
        # Create product description
        description = TextComponent(
            text=product["description"],
            style="margin-bottom: 16px;"
        )
        
        # Create view details button
        view_button = ButtonComponent(
            text="View Details",
            action="view_product",
            component_id="product-list",
            style="""
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            """
        )
        view_button.attributes["data-product-id"] = str(product["id"])
        
        # Add components to the card
        card.add_children(name, category, price, description, view_button)
        
        self.add_child(card)


class ProductDetail(Component):
    """A component representing a detailed view of a product."""
    
    def __init__(self, product: Dict[str, Any], id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.product = product
        
        # Create a container
        container = ContainerComponent(
            style="""
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 24px;
                margin: 16px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            """
        )
        
        # Create back button
        back_button = ButtonComponent(
            text="← Back to Products",
            action="show_products",
            component_id="product-list",
            style="""
                padding: 8px 16px;
                background-color: #f1f1f1;
                color: #333;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-bottom: 16px;
            """
        )
        
        # Create product name
        name = TextComponent(
            text=product["name"],
            tag="h2",
            style="margin-top: 0; margin-bottom: 16px;"
        )
        
        # Create product details
        details = ContainerComponent()
        
        category = TextComponent(
            text=f"Category: {product['category']}",
            style="margin-bottom: 8px;"
        )
        
        price = TextComponent(
            text=f"Price: ${product['price']:.2f}",
            style="margin-bottom: 8px; font-weight: bold; color: #4CAF50;"
        )
        
        description_title = TextComponent(
            text="Description:",
            tag="h3",
            style="margin-bottom: 8px;"
        )
        
        description = TextComponent(
            text=product["description"],
            style="line-height: 1.5;"
        )
        
        # Add components to the details container
        details.add_children(category, price, description_title, description)
        
        # Add components to the main container
        container.add_children(back_button, name, details)
        
        self.add_child(container)


class FilterForm(Component):
    """A component representing a filter form for products."""
    
    def __init__(self, categories: List[str], current_filter: Dict[str, Any] = None, 
                id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.categories = categories
        self.current_filter = current_filter or {}
        
        # Create a form component
        form = FormComponent(
            action="filter_products",
            component_id="product-list",
            style="""
                padding: 16px;
                background-color: #f9f9f9;
                border-radius: 8px;
                margin-bottom: 16px;
            """
        )
        
        # Create a title
        title = TextComponent(
            text="Filter Products",
            tag="h3",
            style="margin-top: 0; margin-bottom: 16px;"
        )
        
        # Create filter controls container
        controls = ContainerComponent(
            style="display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-end;"
        )
        
        # Create search input
        search_container = ContainerComponent(
            style="flex: 1; min-width: 200px;"
        )
        search_label = TextComponent(
            text="Search",
            tag="label",
            style="display: block; margin-bottom: 8px;"
        )
        search_input = InputComponent(
            name="search",
            placeholder="Search by name",
            value=self.current_filter.get("search", ""),
            style="""
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            """
        )
        search_container.add_children(search_label, search_input)
        
        # Create category select
        category_container = ContainerComponent(
            style="flex: 1; min-width: 200px;"
        )
        category_label = TextComponent(
            text="Category",
            tag="label",
            style="display: block; margin-bottom: 8px;"
        )
        
        # Create a select input for categories
        # Since we don't have a native select component, we'll use buttons for each category
        category_buttons = ContainerComponent(
            style="display: flex; flex-wrap: wrap; gap: 8px;"
        )
        
        # Add "All" category button
        all_button = ButtonComponent(
            text="All",
            action="set_category",
            component_id="product-list",
            style=f"""
                padding: 8px 16px;
                background-color: {
                    '#4CAF50' if self.current_filter.get('category') is None else '#f1f1f1'
                };
                color: {
                    'white' if self.current_filter.get('category') is None else '#333'
                };
                border: none;
                border-radius: 4px;
                cursor: pointer;
            """
        )
        all_button.attributes["data-category"] = ""
        category_buttons.add_child(all_button)
        
        # Add category buttons
        for category in categories:
            category_button = ButtonComponent(
                text=category,
                action="set_category",
                component_id="product-list",
                style=f"""
                    padding: 8px 16px;
                    background-color: {
                        '#4CAF50' if self.current_filter.get('category') == category else '#f1f1f1'
                    };
                    color: {
                        'white' if self.current_filter.get('category') == category else '#333'
                    };
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                """
            )
            category_button.attributes["data-category"] = category
            category_buttons.add_child(category_button)
        
        category_container.add_children(category_label, category_buttons)
        
        # Create price range inputs
        price_container = ContainerComponent(
            style="flex: 1; min-width: 200px;"
        )
        price_label = TextComponent(
            text="Price Range",
            tag="label",
            style="display: block; margin-bottom: 8px;"
        )
        price_inputs = ContainerComponent(
            style="display: flex; gap: 8px; align-items: center;"
        )
        min_price_input = InputComponent(
            name="min_price",
            placeholder="Min",
            value=str(self.current_filter.get("min_price", "")),
            input_type="number",
            style="""
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            """
        )
        to_text = TextComponent(
            text="to",
            style="margin: 0 4px;"
        )
        max_price_input = InputComponent(
            name="max_price",
            placeholder="Max",
            value=str(self.current_filter.get("max_price", "")),
            input_type="number",
            style="""
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            """
        )
        price_inputs.add_children(min_price_input, to_text, max_price_input)
        price_container.add_children(price_label, price_inputs)
        
        # Create apply filter button
        apply_button = ButtonComponent(
            text="Apply Filters",
            action="",  # Not needed for form submit
            component_id="",  # Not needed for form submit
            style="""
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            """
        )
        
        # Add components to the controls container
        controls.add_children(search_container, category_container, price_container)
        
        # Add components to the form
        form.add_children(title, controls, apply_button)
        
        self.add_child(form)


class ProductList(Component):
    """A component representing a list of products with filtering and sorting."""
    
    def __init__(self, products: List[Dict[str, Any]] = None, filter_data: Dict[str, Any] = None, 
                selected_product: Optional[Dict[str, Any]] = None, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.products = products or PRODUCTS
        self.filter_data = filter_data or {}
        self.selected_product = selected_product
        
        # Create a container
        container = ContainerComponent(
            style="""
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            """
        )
        
        # Create a title
        title = TextComponent(
            text="Product Catalog",
            tag="h1",
            style="text-align: center; margin-bottom: 24px;"
        )
        
        # If a product is selected, show the product detail view
        if self.selected_product:
            product_detail = ProductDetail(self.selected_product)
            container.add_children(title, product_detail)
        else:
            # Get unique categories
            categories = sorted(set(product["category"] for product in self.products))
            
            # Create filter form
            filter_form = FilterForm(categories, self.filter_data)
            
            # Filter products
            filtered_products = self.filter_products(self.products, self.filter_data)
            
            # Create product count
            product_count = TextComponent(
                text=f"Showing {len(filtered_products)} products",
                style="margin-bottom: 16px; color: #666;"
            )
            
            # Create product cards container
            product_cards = ContainerComponent()
            
            # Create product cards
            for product in filtered_products:
                product_card = ProductCard(product)
                product_cards.add_child(product_card)
            
            # Add components to the container
            container.add_children(title, filter_form, product_count, product_cards)
        
        self.add_child(container)
    
    def filter_products(self, products: List[Dict[str, Any]], filter_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter products based on filter data."""
        result = products
        
        # Filter by search term
        search = filter_data.get("search", "").lower()
        if search:
            result = [
                p for p in result 
                if search in p["name"].lower() or search in p["description"].lower()
            ]
        
        # Filter by category
        category = filter_data.get("category")
        if category:
            result = [p for p in result if p["category"] == category]
        
        # Filter by min price
        min_price = filter_data.get("min_price")
        if min_price and min_price.isdigit():
            min_price = float(min_price)
            result = [p for p in result if p["price"] >= min_price]
        
        # Filter by max price
        max_price = filter_data.get("max_price")
        if max_price and max_price.isdigit():
            max_price = float(max_price)
            result = [p for p in result if p["price"] <= max_price]
        
        return result
    
    def set_category(self, category: str):
        """Set the category filter."""
        new_filter = dict(self.filter_data)
        if category:
            new_filter["category"] = category
        else:
            new_filter.pop("category", None)
        
        return ProductList(filter_data=new_filter, id=self.id)
    
    def filter_products_action(self, filter_data: Dict[str, Any]):
        """Apply filter to products."""
        return ProductList(filter_data=filter_data, id=self.id)
    
    def view_product(self, product_id: str):
        """View a product's details."""
        product_id = int(product_id)
        product = next((p for p in self.products if p["id"] == product_id), None)
        
        if product:
            return ProductList(selected_product=product, filter_data=self.filter_data, id=self.id)
        
        return self
    
    def show_products(self):
        """Show the product list."""
        return ProductList(filter_data=self.filter_data, id=self.id)


def create_product_catalog_app():
    """Create and configure the product catalog app."""
    app = create_app(__name__)
    
    # Create the root component
    product_list = ProductList(id="product-list")
    
    # Set the root component
    app.set_root_component(product_list)
    
    # Register action handlers
    app.register_component_action("product-list", "filter_products", 
                                 lambda c, d: c.filter_products_action(d))
    
    app.register_component_action("product-list", "set_category", 
                                 lambda c, d: c.set_category(d.get("data-category", "")))
    
    app.register_component_action("product-list", "view_product", 
                                 lambda c, d: c.view_product(d.get("data-product-id", "")))
    
    app.register_component_action("product-list", "show_products", 
                                 lambda c, d: c.show_products())
    
    return app


if __name__ == "__main__":
    app = create_product_catalog_app()
    app.run(debug=True)