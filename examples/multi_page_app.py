"""
A multi-page application example using corex.

This example demonstrates how to create a multi-page application with navigation using corex components.
"""
import sys
import os

# Add the parent directory to the path so we can import corex
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.corex import (
    Component,
    CorexApp,
    create_app,
    TextComponent,
    ButtonComponent,
    ContainerComponent,
)


class NavLink(Component):
    """A component representing a navigation link."""
    
    def __init__(self, text: str, page_id: str, current_page_id: str, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.text = text
        self.page_id = page_id
        self.is_active = page_id == current_page_id
        
        # Set the style based on whether this is the active page
        style = """
            padding: 10px 15px;
            text-decoration: none;
            color: #fff;
            background-color: #333;
            margin-right: 5px;
            border-radius: 4px;
        """
        
        if self.is_active:
            style += "background-color: #4CAF50;"
        
        # Create the button component
        button = ButtonComponent(
            text=text,
            action="navigate",
            component_id="app",  # The app component will handle navigation
            style=style
        )
        
        # Add data attribute for the page ID
        button.attributes["data-page-id"] = page_id
        
        self.add_child(button)


class Navbar(Component):
    """A component representing a navigation bar."""
    
    def __init__(self, current_page_id: str, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.current_page_id = current_page_id
        
        # Create a container for the navbar
        container = ContainerComponent(
            style="""
                display: flex;
                background-color: #333;
                padding: 10px;
                margin-bottom: 20px;
            """
        )
        
        # Create navigation links
        home_link = NavLink("Home", "home", current_page_id)
        about_link = NavLink("About", "about", current_page_id)
        contact_link = NavLink("Contact", "contact", current_page_id)
        
        # Add links to the container
        container.add_children(home_link, about_link, contact_link)
        
        self.add_child(container)


class HomePage(Component):
    """A component representing the home page."""
    
    def __init__(self, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Create a container for the page content
        container = ContainerComponent(
            style="padding: 20px;"
        )
        
        # Create page content
        title = TextComponent(
            text="Welcome to the Home Page",
            tag="h1"
        )
        
        content = TextComponent(
            text="""
                This is the home page of our multi-page application.
                Use the navigation bar above to explore different pages.
            """
        )
        
        # Add content to the container
        container.add_children(title, content)
        
        self.add_child(container)


class AboutPage(Component):
    """A component representing the about page."""
    
    def __init__(self, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Create a container for the page content
        container = ContainerComponent(
            style="padding: 20px;"
        )
        
        # Create page content
        title = TextComponent(
            text="About Us",
            tag="h1"
        )
        
        content = TextComponent(
            text="""
                This is the about page of our multi-page application.
                We are a company that specializes in building web applications using corex.
            """
        )
        
        # Add content to the container
        container.add_children(title, content)
        
        self.add_child(container)


class ContactPage(Component):
    """A component representing the contact page."""
    
    def __init__(self, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Create a container for the page content
        container = ContainerComponent(
            style="padding: 20px;"
        )
        
        # Create page content
        title = TextComponent(
            text="Contact Us",
            tag="h1"
        )
        
        content = TextComponent(
            text="""
                This is the contact page of our multi-page application.
                You can reach us at contact@example.com.
            """
        )
        
        # Add content to the container
        container.add_children(title, content)
        
        self.add_child(container)


class App(Component):
    """A component representing the entire application."""
    
    def __init__(self, current_page_id: str = "home", id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.current_page_id = current_page_id
        
        # Create a container for the app
        container = ContainerComponent(
            style="""
                max-width: 800px;
                margin: 0 auto;
                font-family: Arial, sans-serif;
            """
        )
        
        # Create the navbar
        navbar = Navbar(current_page_id)
        
        # Create the current page
        if current_page_id == "home":
            page = HomePage()
        elif current_page_id == "about":
            page = AboutPage()
        elif current_page_id == "contact":
            page = ContactPage()
        else:
            page = HomePage()
        
        # Add navbar and page to the container
        container.add_children(navbar, page)
        
        self.add_child(container)
    
    def navigate(self, page_id: str):
        """Navigate to a different page."""
        return App(current_page_id=page_id, id=self.id)


def create_multi_page_app():
    """Create and configure the multi-page app."""
    app = create_app(__name__)
    
    # Create the root component
    root = App(id="app")
    
    # Set the root component
    app.set_root_component(root)
    
    # Register action handlers
    def navigate_handler(component, data):
        page_id = data.get("data-page-id", "home")
        return component.navigate(page_id)
    
    app.register_component_action("app", "navigate", navigate_handler)
    
    return app


if __name__ == "__main__":
    app = create_multi_page_app()
    app.run(debug=True)