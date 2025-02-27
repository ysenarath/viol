"""
Script to run all corex examples.

This script provides a simple menu to run any of the example applications.
"""
import os
import sys
import importlib.util
import subprocess
from typing import Dict, Callable, List, Tuple


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_examples() -> List[Tuple[str, str, str]]:
    """
    Get a list of example files.
    
    Returns:
        A list of tuples containing (file_name, module_name, description)
    """
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    examples = []
    
    for file_name in os.listdir(examples_dir):
        if file_name.endswith('.py') and file_name != 'run_examples.py' and file_name != '__init__.py':
            module_name = file_name[:-3]  # Remove .py extension
            file_path = os.path.join(examples_dir, file_name)
            
            # Extract the description from the module docstring
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            description = module.__doc__.split('\n')[0] if module.__doc__ else "No description available"
            
            examples.append((file_name, module_name, description))
    
    return sorted(examples)


def display_menu(examples: List[Tuple[str, str, str]]):
    """Display the menu of examples."""
    clear_screen()
    print("=== Corex Examples ===\n")
    
    for i, (_, module_name, description) in enumerate(examples, 1):
        print(f"{i}. {module_name}: {description}")
    
    print("\n0. Exit")
    print("\nEnter the number of the example you want to run:")


def run_example(example_file: str):
    """
    Run an example file.
    
    Args:
        example_file: The file name of the example to run.
    """
    clear_screen()
    print(f"Running {example_file}...\n")
    print("Press Ctrl+C to stop the example and return to the menu.\n")
    
    try:
        # Run the example in a subprocess
        examples_dir = os.path.dirname(os.path.abspath(__file__))
        example_path = os.path.join(examples_dir, example_file)
        
        subprocess.run([sys.executable, example_path], check=True)
    except KeyboardInterrupt:
        print("\nExample stopped.")
    except subprocess.CalledProcessError as e:
        print(f"\nError running example: {e}")
    
    input("\nPress Enter to return to the menu...")


def main():
    """Main function to run the examples menu."""
    examples = get_examples()
    
    while True:
        display_menu(examples)
        
        try:
            choice = input().strip()
            
            if choice == '0':
                clear_screen()
                print("Goodbye!")
                break
            
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(examples):
                    run_example(examples[choice_idx][0])
                else:
                    print("Invalid choice. Press Enter to continue...")
                    input()
            except ValueError:
                print("Please enter a number. Press Enter to continue...")
                input()
        
        except KeyboardInterrupt:
            clear_screen()
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()