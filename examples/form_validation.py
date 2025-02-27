"""
A form validation example using corex.

This example demonstrates how to create a form with validation using corex components.
"""
import sys
import os
import re

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
)


class ValidationMessage(Component):
    """A component for displaying validation messages."""
    
    def __init__(self, message: str, is_error: bool = False, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.message = message
        self.is_error = is_error
        
        # Set the style based on whether this is an error or success message
        color = "#f44336" if is_error else "#4CAF50"
        
        # Create the message component
        message_component = TextComponent(
            text=message,
            style=f"color: {color}; margin-top: 5px; font-size: 14px;"
        )
        
        self.add_child(message_component)


class FormField(Component):
    """A component representing a form field with label and validation."""
    
    def __init__(self, name: str, label: str, input_type: str = "text", 
                required: bool = False, validation_message: str = None,
                id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.name = name
        self.label = label
        self.input_type = input_type
        self.required = required
        self.validation_message = validation_message
        
        # Create a container for the field
        container = ContainerComponent(
            style="margin-bottom: 15px;"
        )
        
        # Create the label
        label_text = f"{label}{' *' if required else ''}"
        label_component = TextComponent(
            text=label_text,
            tag="label",
            style="display: block; margin-bottom: 5px; font-weight: bold;"
        )
        
        # Create the input
        input_component = InputComponent(
            name=name,
            input_type=input_type,
            style="width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;"
        )
        
        # Add components to the container
        container.add_children(label_component, input_component)
        
        # Add validation message if provided
        if validation_message:
            validation_component = ValidationMessage(
                message=validation_message,
                is_error=True
            )
            container.add_child(validation_component)
        
        self.add_child(container)


class RegistrationForm(Component):
    """A component representing a registration form with validation."""
    
    def __init__(self, validation_errors: dict = None, success_message: str = None, 
                id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.validation_errors = validation_errors or {}
        self.success_message = success_message
        
        # Create a container with centered content
        container = ContainerComponent(
            style="max-width: 500px; margin: 50px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
        )
        
        # Create a title
        title = TextComponent(
            text="Registration Form",
            tag="h1",
            style="margin-top: 0; margin-bottom: 20px; text-align: center;"
        )
        
        # Create the form
        form = FormComponent(
            action="submit",
            component_id=self.id,
            style="width: 100%;"
        )
        
        # Create form fields
        name_field = FormField(
            name="name",
            label="Name",
            required=True,
            validation_message=self.validation_errors.get("name")
        )
        
        email_field = FormField(
            name="email",
            label="Email",
            input_type="email",
            required=True,
            validation_message=self.validation_errors.get("email")
        )
        
        password_field = FormField(
            name="password",
            label="Password",
            input_type="password",
            required=True,
            validation_message=self.validation_errors.get("password")
        )
        
        confirm_password_field = FormField(
            name="confirm_password",
            label="Confirm Password",
            input_type="password",
            required=True,
            validation_message=self.validation_errors.get("confirm_password")
        )
        
        # Create submit button
        submit_button = ButtonComponent(
            text="Register",
            action="",  # Not needed for form submit
            component_id="",  # Not needed for form submit
            style="width: 100%; padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 10px;"
        )
        
        # Add fields and button to the form
        form.add_children(
            name_field,
            email_field,
            password_field,
            confirm_password_field,
            submit_button
        )
        
        # Add title and form to the container
        container.add_children(title, form)
        
        # Add success message if provided
        if success_message:
            success_component = ValidationMessage(
                message=success_message,
                is_error=False,
                style="text-align: center; margin-top: 15px;"
            )
            container.add_child(success_component)
        
        self.add_child(container)


def validate_registration_form(data):
    """Validate the registration form data."""
    errors = {}
    
    # Validate name
    name = data.get("name", "").strip()
    if not name:
        errors["name"] = "Name is required"
    
    # Validate email
    email = data.get("email", "").strip()
    if not email:
        errors["email"] = "Email is required"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors["email"] = "Invalid email format"
    
    # Validate password
    password = data.get("password", "")
    if not password:
        errors["password"] = "Password is required"
    elif len(password) < 8:
        errors["password"] = "Password must be at least 8 characters"
    
    # Validate confirm password
    confirm_password = data.get("confirm_password", "")
    if not confirm_password:
        errors["confirm_password"] = "Confirm password is required"
    elif password != confirm_password:
        errors["confirm_password"] = "Passwords do not match"
    
    return errors


def create_registration_app():
    """Create and configure the registration app."""
    app = create_app(__name__)
    
    # Create the root component
    form = RegistrationForm(id="registration-form")
    
    # Set the root component
    app.set_root_component(form)
    
    # Register action handlers
    def submit_handler(component, data):
        # Validate the form data
        errors = validate_registration_form(data)
        
        if errors:
            # If there are errors, return a new form with validation errors
            return RegistrationForm(validation_errors=errors, id=component.id)
        else:
            # If validation passes, return a new form with a success message
            return RegistrationForm(
                success_message="Registration successful! Thank you for registering.",
                id=component.id
            )
    
    app.register_component_action("registration-form", "submit", submit_handler)
    
    return app


if __name__ == "__main__":
    app = create_registration_app()
    app.run(debug=True)