"""
Tests for the Component class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import corex
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.corex import Component, TextComponent


class TestComponent(unittest.TestCase):
    """Test cases for the Component class."""
    
    def test_component_initialization(self):
        """Test that a component can be initialized with an ID."""
        component = Component(id="test-id")
        self.assertEqual(component.id, "test-id")
        self.assertEqual(component.children, [])
        self.assertIsNone(component.parent)
    
    def test_component_initialization_without_id(self):
        """Test that a component can be initialized without an ID."""
        component = Component()
        self.assertIsNotNone(component.id)
        self.assertTrue(len(component.id) > 0)
    
    def test_add_child(self):
        """Test that a child component can be added to a parent component."""
        parent = Component(id="parent")
        child = Component(id="child")
        
        parent.add_child(child)
        
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)
        self.assertEqual(child.parent, parent)
    
    def test_add_children(self):
        """Test that multiple child components can be added to a parent component."""
        parent = Component(id="parent")
        child1 = Component(id="child1")
        child2 = Component(id="child2")
        
        parent.add_children(child1, child2)
        
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)
    
    def test_replace_with(self):
        """Test that a component can be replaced with another component."""
        parent = Component(id="parent")
        child1 = Component(id="child1")
        child2 = Component(id="child2")
        
        parent.add_child(child1)
        child1.replace_with(child2)
        
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child2)
        self.assertEqual(child2.parent, parent)
        self.assertIsNone(child1.parent)
    
    def test_find_by_id(self):
        """Test that a component can be found by its ID."""
        parent = Component(id="parent")
        child1 = Component(id="child1")
        child2 = Component(id="child2")
        grandchild = Component(id="grandchild")
        
        parent.add_child(child1)
        parent.add_child(child2)
        child1.add_child(grandchild)
        
        self.assertEqual(parent.find_by_id("parent"), parent)
        self.assertEqual(parent.find_by_id("child1"), child1)
        self.assertEqual(parent.find_by_id("child2"), child2)
        self.assertEqual(parent.find_by_id("grandchild"), grandchild)
        self.assertIsNone(parent.find_by_id("nonexistent"))
    
    def test_render(self):
        """Test that a component can be rendered to HTML."""
        component = Component(id="test-id", class_="test-class")
        html = component.render()
        
        self.assertIn('id="test-id"', html)
        self.assertIn('class_="test-class"', html)
    
    def test_text_component_render(self):
        """Test that a TextComponent can be rendered to HTML."""
        component = TextComponent(text="Hello, world!", tag="h1", id="test-id")
        html = component.render()
        
        self.assertIn('id="test-id"', html)
        self.assertIn('<h1', html)
        self.assertIn('</h1>', html)
        self.assertIn('Hello, world!', html)


if __name__ == "__main__":
    unittest.main()