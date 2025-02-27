"""
A simple todo app example using corex.

This example demonstrates how to create a todo application using corex components.
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
    InputComponent,
    FormComponent,
    CardComponent,
    ListComponent,
)


class TodoItem(Component):
    """A component representing a single todo item."""
    
    def __init__(self, text: str, completed: bool = False, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.text = text
        self.completed = completed
        
        # Style based on completion status
        style = "text-decoration: line-through;" if completed else ""
        
        # Create the text component for the todo item
        text_component = TextComponent(
            text=text,
            style=style
        )
        
        # Create toggle button
        toggle_text = "✓" if not completed else "↻"
        toggle_button = ButtonComponent(
            text=toggle_text,
            action="toggle",
            component_id=self.id,
            style="margin-left: 10px; cursor: pointer;"
        )
        
        # Create delete button
        delete_button = ButtonComponent(
            text="🗑",
            action="delete",
            component_id=self.id,
            style="margin-left: 10px; cursor: pointer;"
        )
        
        # Add components to container
        container = ContainerComponent(
            style="display: flex; align-items: center; margin: 5px 0;"
        )
        container.add_children(text_component, toggle_button, delete_button)
        self.add_child(container)
    
    def toggle(self):
        """Toggle the completed status of this todo item."""
        return TodoItem(self.text, not self.completed, self.id)


class TodoList(Component):
    """A component representing a list of todo items."""
    
    def __init__(self, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Create a title
        title = TextComponent(
            text="Todo List",
            tag="h1"
        )
        
        # Create a form for adding new todos
        form = FormComponent(
            action="add_todo",
            component_id=self.id
        )
        
        # Create an input for the new todo text
        input_field = InputComponent(
            name="todo_text",
            placeholder="Enter a new todo item",
            style="padding: 8px; margin-right: 10px; width: 300px;"
        )
        
        # Create a submit button
        submit_button = ButtonComponent(
            text="Add",
            action="",  # Not needed for form submit
            component_id="",  # Not needed for form submit
            style="padding: 8px 16px; background-color: #4CAF50; color: white; border: none; cursor: pointer;"
        )
        
        # Add the input and button to the form
        form.add_children(input_field, submit_button)
        
        # Create a container for the todo items
        items_container = ContainerComponent(id="todo-items")
        
        # Add all components to the todo list
        self.add_children(title, form, items_container)


def create_todo_app():
    """Create and configure the todo app."""
    app = create_app(__name__)
    
    # Create the root component
    todo_list = TodoList(id="todo-list")
    
    # Set the root component
    app.set_root_component(todo_list)
    
    # Register action handlers
    
    # Handler for adding a new todo
    def add_todo_handler(component, data):
        todo_text = data.get("todo_text", "").strip()
        if not todo_text:
            return component
        
        # Find the items container
        items_container = component.find_by_id("todo-items")
        if items_container:
            # Create a new todo item and add it to the container
            todo_item = TodoItem(text=todo_text)
            items_container.add_child(todo_item)
            
            # Register actions for the new todo item
            app.register_component_action(todo_item.id, "toggle", toggle_todo_handler)
            app.register_component_action(todo_item.id, "delete", delete_todo_handler)
        
        return component
    
    # Handler for toggling a todo item
    def toggle_todo_handler(component, data):
        return component.toggle()
    
    # Handler for deleting a todo item
    def delete_todo_handler(component, data):
        if component.parent and component.parent.parent:
            # Remove the todo item from its parent
            parent = component.parent.parent
            parent.children.remove(component.parent)
        return component.parent.parent if component.parent and component.parent.parent else component
    
    # Register the add_todo action for the todo list
    app.register_component_action("todo-list", "add_todo", add_todo_handler)
    
    return app


if __name__ == "__main__":
    app = create_todo_app()
    app.run(debug=True)