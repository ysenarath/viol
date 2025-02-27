"""
Custom components example using corex.

This example demonstrates how to create custom components with custom rendering.
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
)


class ProgressBar(Component):
    """A custom component that renders a progress bar."""
    
    def __init__(self, value: int = 0, max_value: int = 100, 
                color: str = "#4CAF50", id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.value = max(0, min(value, max_value))  # Clamp value between 0 and max_value
        self.max_value = max_value
        self.color = color
    
    def render(self) -> str:
        """
        Render this component to HTML.
        
        Returns:
            The HTML representation of this component.
        """
        # Calculate the percentage
        percentage = (self.value / self.max_value) * 100
        
        # Create the HTML for the progress bar
        html = f'''
            <div id="{self.id}" class="progress-container" style="
                width: 100%;
                background-color: #f1f1f1;
                border-radius: 4px;
                margin: 10px 0;
                overflow: hidden;
            ">
                <div class="progress-bar" style="
                    width: {percentage}%;
                    height: 20px;
                    background-color: {self.color};
                    text-align: center;
                    line-height: 20px;
                    color: white;
                    transition: width 0.5s ease-in-out;
                ">
                    {int(percentage)}%
                </div>
            </div>
        '''
        
        return html


class Rating(Component):
    """A custom component that renders a star rating system."""
    
    def __init__(self, value: int = 0, max_value: int = 5, 
                id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.value = max(0, min(value, max_value))  # Clamp value between 0 and max_value
        self.max_value = max_value
    
    def render(self) -> str:
        """
        Render this component to HTML.
        
        Returns:
            The HTML representation of this component.
        """
        # Create the HTML for the rating
        stars_html = ""
        for i in range(1, self.max_value + 1):
            # Determine if this star should be filled or empty
            filled = i <= self.value
            
            # Create the star HTML with HTMX to handle clicks
            star_html = f'''
                <span 
                    class="star {'filled' if filled else 'empty'}" 
                    hx-post="/components/{self.id}/action/set_rating"
                    hx-trigger="click"
                    hx-target="#{self.id}"
                    hx-swap="outerHTML"
                    hx-vals='{{"rating": {i}}}'
                    style="
                        font-size: 24px;
                        cursor: pointer;
                        color: {('#FFD700' if filled else '#ccc')};
                        margin-right: 5px;
                    "
                >
                    ★
                </span>
            '''
            
            stars_html += star_html
        
        # Create the container HTML
        html = f'''
            <div id="{self.id}" class="rating-container" style="
                display: inline-block;
                margin: 10px 0;
            ">
                {stars_html}
                <span style="margin-left: 10px; font-size: 14px; color: #666;">
                    {self.value} of {self.max_value}
                </span>
            </div>
        '''
        
        return html
    
    def set_rating(self, rating: int):
        """Set the rating value."""
        return Rating(value=int(rating), max_value=self.max_value, id=self.id)


class Accordion(Component):
    """A custom component that renders an accordion with collapsible sections."""
    
    def __init__(self, sections: List[Dict[str, str]], 
                active_section: int = None, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.sections = sections
        self.active_section = active_section
    
    def render(self) -> str:
        """
        Render this component to HTML.
        
        Returns:
            The HTML representation of this component.
        """
        # Create the HTML for the accordion
        sections_html = ""
        
        for i, section in enumerate(self.sections):
            # Determine if this section is active
            is_active = i == self.active_section
            
            # Create the section HTML with HTMX to handle clicks
            section_html = f'''
                <div class="accordion-section" style="
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-bottom: 5px;
                    overflow: hidden;
                ">
                    <div 
                        class="accordion-header" 
                        hx-post="/components/{self.id}/action/toggle_section"
                        hx-trigger="click"
                        hx-target="#{self.id}"
                        hx-swap="outerHTML"
                        hx-vals='{{"section": {i}}}'
                        style="
                            padding: 10px 15px;
                            background-color: #f1f1f1;
                            cursor: pointer;
                            font-weight: bold;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        "
                    >
                        {section['title']}
                        <span style="
                            font-size: 18px;
                            transition: transform 0.3s ease;
                            transform: rotate({('90' if is_active else '0')}deg);
                        ">
                            ›
                        </span>
                    </div>
                    <div class="accordion-content" style="
                        padding: {('15px' if is_active else '0 15px')};
                        max-height: {('1000px' if is_active else '0')};
                        overflow: hidden;
                        transition: all 0.3s ease;
                    ">
                        {section['content'] if is_active else ''}
                    </div>
                </div>
            '''
            
            sections_html += section_html
        
        # Create the container HTML
        html = f'''
            <div id="{self.id}" class="accordion-container" style="
                width: 100%;
                margin: 10px 0;
            ">
                {sections_html}
            </div>
        '''
        
        return html
    
    def toggle_section(self, section: int):
        """Toggle a section open or closed."""
        section = int(section)
        new_active = section if section != self.active_section else None
        return Accordion(sections=self.sections, active_section=new_active, id=self.id)


class Tabs(Component):
    """A custom component that renders a tabbed interface."""
    
    def __init__(self, tabs: List[Dict[str, str]], 
                active_tab: int = 0, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.tabs = tabs
        self.active_tab = active_tab if 0 <= active_tab < len(tabs) else 0
    
    def render(self) -> str:
        """
        Render this component to HTML.
        
        Returns:
            The HTML representation of this component.
        """
        # Create the HTML for the tabs
        tabs_html = ""
        
        # Create the tab headers
        tabs_header_html = '<div class="tabs-header" style="display: flex; border-bottom: 1px solid #ddd;">'
        
        for i, tab in enumerate(self.tabs):
            # Determine if this tab is active
            is_active = i == self.active_tab
            
            # Create the tab header HTML with HTMX to handle clicks
            tab_header_html = f'''
                <div 
                    class="tab-header {('active' if is_active else '')}" 
                    hx-post="/components/{self.id}/action/switch_tab"
                    hx-trigger="click"
                    hx-target="#{self.id}"
                    hx-swap="outerHTML"
                    hx-vals='{{"tab": {i}}}'
                    style="
                        padding: 10px 15px;
                        cursor: pointer;
                        {('border-bottom: 2px solid #4CAF50; font-weight: bold;' if is_active else '')}
                    "
                >
                    {tab['title']}
                </div>
            '''
            
            tabs_header_html += tab_header_html
        
        tabs_header_html += '</div>'
        
        # Create the tab content
        active_tab_content = self.tabs[self.active_tab]['content']
        tabs_content_html = f'''
            <div class="tabs-content" style="
                padding: 15px;
                border: 1px solid #ddd;
                border-top: none;
            ">
                {active_tab_content}
            </div>
        '''
        
        # Combine the header and content
        tabs_html = tabs_header_html + tabs_content_html
        
        # Create the container HTML
        html = f'''
            <div id="{self.id}" class="tabs-container" style="
                width: 100%;
                margin: 10px 0;
            ">
                {tabs_html}
            </div>
        '''
        
        return html
    
    def switch_tab(self, tab: int):
        """Switch to a different tab."""
        return Tabs(tabs=self.tabs, active_tab=int(tab), id=self.id)


class CustomComponentsDemo(Component):
    """A component that demonstrates various custom components."""
    
    def __init__(self, id: str = None, **kwargs):
        super().__init__(id=id, **kwargs)
        
        # Create a container with centered content
        container = ContainerComponent(
            style="""
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                font-family: Arial, sans-serif;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            """
        )
        
        # Create a title
        title = TextComponent(
            text="Custom Components Demo",
            tag="h1",
            style="text-align: center; margin-bottom: 30px;"
        )
        
        # Create sections for each custom component
        progress_section = self.create_progress_section()
        rating_section = self.create_rating_section()
        accordion_section = self.create_accordion_section()
        tabs_section = self.create_tabs_section()
        
        # Add all sections to the container
        container.add_children(
            title,
            progress_section,
            rating_section,
            accordion_section,
            tabs_section
        )
        
        self.add_child(container)
    
    def create_progress_section(self):
        """Create a section demonstrating the ProgressBar component."""
        section = ContainerComponent(
            style="margin-bottom: 30px;"
        )
        
        title = TextComponent(
            text="Progress Bar Component",
            tag="h2"
        )
        
        description = TextComponent(
            text="A custom component that renders a progress bar with customizable value and color."
        )
        
        # Create progress bars with different values and colors
        progress1 = ProgressBar(value=25, max_value=100, color="#4CAF50")
        progress2 = ProgressBar(value=50, max_value=100, color="#2196F3")
        progress3 = ProgressBar(value=75, max_value=100, color="#FF9800")
        progress4 = ProgressBar(value=100, max_value=100, color="#F44336")
        
        # Add components to the section
        section.add_children(
            title,
            description,
            progress1,
            progress2,
            progress3,
            progress4
        )
        
        return section
    
    def create_rating_section(self):
        """Create a section demonstrating the Rating component."""
        section = ContainerComponent(
            style="margin-bottom: 30px;"
        )
        
        title = TextComponent(
            text="Rating Component",
            tag="h2"
        )
        
        description = TextComponent(
            text="A custom component that renders a star rating system. Click on a star to set the rating."
        )
        
        # Create ratings with different values
        rating1 = Rating(value=0, max_value=5, id="rating1")
        rating2 = Rating(value=3, max_value=5, id="rating2")
        rating3 = Rating(value=5, max_value=5, id="rating3")
        
        # Add components to the section
        section.add_children(
            title,
            description,
            rating1,
            TextComponent(text="<br>"),
            rating2,
            TextComponent(text="<br>"),
            rating3
        )
        
        return section
    
    def create_accordion_section(self):
        """Create a section demonstrating the Accordion component."""
        section = ContainerComponent(
            style="margin-bottom: 30px;"
        )
        
        title = TextComponent(
            text="Accordion Component",
            tag="h2"
        )
        
        description = TextComponent(
            text="A custom component that renders an accordion with collapsible sections. Click on a section header to expand or collapse it."
        )
        
        # Create accordion sections
        sections = [
            {
                "title": "Section 1",
                "content": "This is the content for section 1. It can contain any HTML content."
            },
            {
                "title": "Section 2",
                "content": "This is the content for section 2. The accordion will only show one section at a time."
            },
            {
                "title": "Section 3",
                "content": "This is the content for section 3. Clicking on an open section will close it."
            }
        ]
        
        # Create the accordion
        accordion = Accordion(sections=sections, id="accordion")
        
        # Add components to the section
        section.add_children(
            title,
            description,
            accordion
        )
        
        return section
    
    def create_tabs_section(self):
        """Create a section demonstrating the Tabs component."""
        section = ContainerComponent(
            style="margin-bottom: 30px;"
        )
        
        title = TextComponent(
            text="Tabs Component",
            tag="h2"
        )
        
        description = TextComponent(
            text="A custom component that renders a tabbed interface. Click on a tab to switch between content."
        )
        
        # Create tab content
        tabs = [
            {
                "title": "Tab 1",
                "content": "This is the content for tab 1. Tabs are a great way to organize content in a limited space."
            },
            {
                "title": "Tab 2",
                "content": "This is the content for tab 2. Only one tab can be active at a time."
            },
            {
                "title": "Tab 3",
                "content": "This is the content for tab 3. Tabs can contain any HTML content."
            }
        ]
        
        # Create the tabs
        tabs_component = Tabs(tabs=tabs, id="tabs")
        
        # Add components to the section
        section.add_children(
            title,
            description,
            tabs_component
        )
        
        return section


def create_custom_components_app():
    """Create and configure the custom components demo app."""
    app = create_app(__name__)
    
    # Create the root component
    demo = CustomComponentsDemo(id="custom-components-demo")
    
    # Set the root component
    app.set_root_component(demo)
    
    # Register action handlers for the Rating component
    app.register_component_action("rating1", "set_rating", 
                                 lambda c, d: c.set_rating(d.get("rating", 0)))
    
    app.register_component_action("rating2", "set_rating", 
                                 lambda c, d: c.set_rating(d.get("rating", 0)))
    
    app.register_component_action("rating3", "set_rating", 
                                 lambda c, d: c.set_rating(d.get("rating", 0)))
    
    # Register action handlers for the Accordion component
    app.register_component_action("accordion", "toggle_section", 
                                 lambda c, d: c.toggle_section(d.get("section", 0)))
    
    # Register action handlers for the Tabs component
    app.register_component_action("tabs", "switch_tab", 
                                 lambda c, d: c.switch_tab(d.get("tab", 0)))
    
    return app


if __name__ == "__main__":
    app = create_custom_components_app()
    app.run(debug=True)