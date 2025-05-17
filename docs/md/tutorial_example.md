# Building a Task Management Application with Viol

This tutorial will guide you through building a simple but functional task management web application using the Viol package. By the end, you'll have a fully working application that allows users to add, view, and mark tasks as complete.

## Introduction

In this tutorial, we'll build a task management application that demonstrates the core features of Viol. Our application will:

- Display a list of tasks
- Allow users to add new tasks
- Let users mark tasks as complete
- Provide a clean, responsive interface using Bootstrap components

Viol is a Python library for building web applications using a component-based approach. It provides a Pythonic way to create HTML elements and components, with built-in support for Bootstrap UI components and HTMX for interactivity.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Basic knowledge of Python and web development concepts

### Installation

1. Create a new directory for your project:

```bash
mkdir task_manager
cd task_manager
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install viol flask
```

4. Create a basic project structure:

```
task_manager/
├── app.py
├── components/
│   ├── __init__.py
│   ├── task_form.py
│   └── task_list.py
├── models/
│   ├── __init__.py
│   └── task.py
└── static/
    └── css/
        └── custom.css
```

You can create this structure with the following commands:

```bash
mkdir -p components models static/css
touch app.py components/__init__.py components/task_form.py components/task_list.py models/__init__.py models/task.py static/css/custom.css
```

## Step-by-Step Implementation

### Step 1: Setting up the Flask Application

Let's start by creating the basic Flask application with Viol integration. Open `app.py` and add the following code:

```python
from flask import Flask, request, redirect, url_for
import viol
from viol import BasicLayout, html, render
from components.task_form import create_task_form
from components.task_list import create_task_list
from models.task import Task, tasks

app = Flask(__name__)
viol.init_app(app)

@app.route("/")
def home():
    # Create the main page layout
    body = html.div(
        [
            html.div(
                html.h1("Task Manager", attrs={"class": "mb-4"}),
                attrs={"class": "text-center py-3 bg-light"}
            ),
            html.div(
                [
                    create_task_form(),
                    html.hr(),
                    create_task_list(tasks),
                ],
                attrs={"class": "container py-4"}
            )
        ]
    )
    
    return render(BasicLayout(
        body=body,
        title="Task Manager - Viol Example"
    ))

@app.route("/add-task", methods=["POST"])
def add_task():
    task_title = request.form.get("task_title", "").strip()
    if task_title:
        new_task = Task(title=task_title)
        tasks.append(new_task)
    return redirect(url_for("home"))

@app.route("/toggle-task/<task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            break
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
```

### Step 2: Creating the Task Model

Next, let's define our Task model. Open `models/task.py` and add the following code:

```python
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Task:
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

# In-memory storage for tasks
tasks: List[Task] = [
    Task(title="Learn Viol basics"),
    Task(title="Build a task manager app"),
    Task(title="Add Bootstrap styling")
]
```

### Step 3: Creating the Task Form Component

Now, let's create the form for adding new tasks. Open `components/task_form.py` and add the following code:

```python
from viol.html import div, form, input, button, label
from viol.bootstrap.buttons import Button
from flask import url_for

def create_task_form():
    """Create a form for adding new tasks."""
    return div(
        [
            div(
                label("Add a new task:", attrs={"for": "task_title", "class": "form-label fw-bold"}),
                attrs={"class": "mb-2"}
            ),
            form(
                [
                    div(
                        [
                            input(
                                attrs={
                                    "type": "text",
                                    "name": "task_title",
                                    "id": "task_title",
                                    "placeholder": "Enter task description...",
                                    "class": "form-control",
                                    "required": "true"
                                }
                            ),
                        ],
                        attrs={"class": "col-md-9"}
                    ),
                    div(
                        Button(
                            "Add Task",
                            color="primary",
                            attrs={"type": "submit"}
                        ),
                        attrs={"class": "col-md-3"}
                    )
                ],
                attrs={
                    "action": url_for("add_task"),
                    "method": "post",
                    "class": "row g-3 align-items-center"
                }
            )
        ],
        attrs={"class": "mb-4 p-3 bg-light rounded"}
    )
```

### Step 4: Creating the Task List Component

Next, let's create the component for displaying the list of tasks. Open `components/task_list.py` and add the following code:

```python
from viol.html import div, h2, ul, li, form, button, span
from viol.bootstrap.badge import Badge
from viol.core import EventHandler
from flask import url_for
from models.task import Task
from typing import List

def create_task_list(tasks: List[Task]):
    """Create a list of tasks with the ability to mark them as complete."""
    return div(
        [
            div(
                [
                    h2("Your Tasks", attrs={"class": "mb-3"}),
                    div(
                        Badge(str(len([t for t in tasks if not t.completed])), color="primary"),
                        attrs={"class": "ms-2"}
                    ) if tasks else ""
                ],
                attrs={"class": "d-flex align-items-center"}
            ),
            ul(
                [create_task_item(task) for task in tasks] if tasks else 
                [li("No tasks yet. Add one above!", attrs={"class": "list-group-item text-muted"})],
                attrs={"class": "list-group mt-3", "id": "task-list"}
            )
        ],
        attrs={"class": "mt-4"}
    )

def create_task_item(task: Task):
    """Create a single task item."""
    return li(
        [
            div(
                [
                    div(
                        [
                            span(
                                task.title,
                                attrs={
                                    "class": "task-title" + (" text-decoration-line-through text-muted" if task.completed else "")
                                }
                            ),
                            Badge("Completed", color="success", attrs={"class": "ms-2"}) if task.completed else ""
                        ],
                        attrs={"class": "col-10"}
                    ),
                    div(
                        form(
                            button(
                                "✓" if not task.completed else "↺",
                                attrs={
                                    "type": "submit",
                                    "class": f"btn btn-sm btn-{'outline-success' if not task.completed else 'outline-secondary'}"
                                }
                            ),
                            attrs={
                                "action": url_for("toggle_task", task_id=task.id),
                                "method": "post",
                                "class": "d-inline"
                            }
                        ),
                        attrs={"class": "col-2 text-end"}
                    )
                ],
                attrs={"class": "row align-items-center"}
            )
        ],
        attrs={"class": "list-group-item" + (" bg-light" if task.completed else "")}
    )
```

### Step 5: Adding Custom CSS

Let's add some custom CSS to enhance the appearance of our application. Open `static/css/custom.css` and add the following:

```css
.task-title {
    font-size: 1.1rem;
}

.completed {
    text-decoration: line-through;
    color: #6c757d;
}

.list-group-item:hover {
    background-color: #f8f9fa;
}

.btn-outline-success:hover, .btn-outline-secondary:hover {
    transform: scale(1.1);
    transition: transform 0.2s;
}
```

### Step 6: Updating the Layout to Include Custom CSS

Now, let's update our `app.py` file to include the custom CSS in our layout:

```python
# Add this import at the top
from flask import Flask, request, redirect, url_for, url_for

# Update the BasicLayout call in the home route
return render(BasicLayout(
    body=body,
    title="Task Manager - Viol Example",
    extra_head_content=f'<link rel="stylesheet" href="{url_for("static", filename="css/custom.css")}">'
))
```

## Complete Code

Here's the complete code for the application:

### app.py

```python
from flask import Flask, request, redirect, url_for
import viol
from viol import BasicLayout, html, render
from components.task_form import create_task_form
from components.task_list import create_task_list
from models.task import Task, tasks

app = Flask(__name__)
viol.init_app(app)

@app.route("/")
def home():
    # Create the main page layout
    body = html.div(
        [
            html.div(
                html.h1("Task Manager", attrs={"class": "mb-4"}),
                attrs={"class": "text-center py-3 bg-light"}
            ),
            html.div(
                [
                    create_task_form(),
                    html.hr(),
                    create_task_list(tasks),
                ],
                attrs={"class": "container py-4"}
            )
        ]
    )
    
    return render(BasicLayout(
        body=body,
        title="Task Manager - Viol Example",
        extra_head_content=f'<link rel="stylesheet" href="{url_for("static", filename="css/custom.css")}">'
    ))

@app.route("/add-task", methods=["POST"])
def add_task():
    task_title = request.form.get("task_title", "").strip()
    if task_title:
        new_task = Task(title=task_title)
        tasks.append(new_task)
    return redirect(url_for("home"))

@app.route("/toggle-task/<task_id>", methods=["POST"])
def toggle_task(task_id):
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            break
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
```

### models/task.py

```python
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Task:
    title: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

# In-memory storage for tasks
tasks: List[Task] = [
    Task(title="Learn Viol basics"),
    Task(title="Build a task manager app"),
    Task(title="Add Bootstrap styling")
]
```

### components/task_form.py

```python
from viol.html import div, form, input, button, label
from viol.bootstrap.buttons import Button
from flask import url_for

def create_task_form():
    """Create a form for adding new tasks."""
    return div(
        [
            div(
                label("Add a new task:", attrs={"for": "task_title", "class": "form-label fw-bold"}),
                attrs={"class": "mb-2"}
            ),
            form(
                [
                    div(
                        [
                            input(
                                attrs={
                                    "type": "text",
                                    "name": "task_title",
                                    "id": "task_title",
                                    "placeholder": "Enter task description...",
                                    "class": "form-control",
                                    "required": "true"
                                }
                            ),
                        ],
                        attrs={"class": "col-md-9"}
                    ),
                    div(
                        Button(
                            "Add Task",
                            color="primary",
                            attrs={"type": "submit"}
                        ),
                        attrs={"class": "col-md-3"}
                    )
                ],
                attrs={
                    "action": url_for("add_task"),
                    "method": "post",
                    "class": "row g-3 align-items-center"
                }
            )
        ],
        attrs={"class": "mb-4 p-3 bg-light rounded"}
    )
```

### components/task_list.py

```python
from viol.html import div, h2, ul, li, form, button, span
from viol.bootstrap.badge import Badge
from viol.core import EventHandler
from flask import url_for
from models.task import Task
from typing import List

def create_task_list(tasks: List[Task]):
    """Create a list of tasks with the ability to mark them as complete."""
    return div(
        [
            div(
                [
                    h2("Your Tasks", attrs={"class": "mb-3"}),
                    div(
                        Badge(str(len([t for t in tasks if not t.completed])), color="primary"),
                        attrs={"class": "ms-2"}
                    ) if tasks else ""
                ],
                attrs={"class": "d-flex align-items-center"}
            ),
            ul(
                [create_task_item(task) for task in tasks] if tasks else 
                [li("No tasks yet. Add one above!", attrs={"class": "list-group-item text-muted"})],
                attrs={"class": "list-group mt-3", "id": "task-list"}
            )
        ],
        attrs={"class": "mt-4"}
    )

def create_task_item(task: Task):
    """Create a single task item."""
    return li(
        [
            div(
                [
                    div(
                        [
                            span(
                                task.title,
                                attrs={
                                    "class": "task-title" + (" text-decoration-line-through text-muted" if task.completed else "")
                                }
                            ),
                            Badge("Completed", color="success", attrs={"class": "ms-2"}) if task.completed else ""
                        ],
                        attrs={"class": "col-10"}
                    ),
                    div(
                        form(
                            button(
                                "✓" if not task.completed else "↺",
                                attrs={
                                    "type": "submit",
                                    "class": f"btn btn-sm btn-{'outline-success' if not task.completed else 'outline-secondary'}"
                                }
                            ),
                            attrs={
                                "action": url_for("toggle_task", task_id=task.id),
                                "method": "post",
                                "class": "d-inline"
                            }
                        ),
                        attrs={"class": "col-2 text-end"}
                    )
                ],
                attrs={"class": "row align-items-center"}
            )
        ],
        attrs={"class": "list-group-item" + (" bg-light" if task.completed else "")}
    )
```

### static/css/custom.css

```css
.task-title {
    font-size: 1.1rem;
}

.completed {
    text-decoration: line-through;
    color: #6c757d;
}

.list-group-item:hover {
    background-color: #f8f9fa;
}

.btn-outline-success:hover, .btn-outline-secondary:hover {
    transform: scale(1.1);
    transition: transform 0.2s;
}
```

## Running the Application

To run the application, execute the following command in your terminal:

```bash
python app.py
```

This will start the Flask development server. Open your web browser and navigate to `http://127.0.0.1:5000/` to see your task management application in action.

## How It Works

Let's break down how this application works:

1. **Flask Integration**: We use Flask as our web framework and integrate Viol using `viol.init_app(app)`.

2. **Component-Based Architecture**: We organize our UI into reusable components:
   - `task_form.py` contains the form for adding new tasks
   - `task_list.py` contains the list of tasks and individual task items

3. **Data Model**: We use a simple `Task` class to represent our tasks, with in-memory storage for this example.

4. **Routing and Actions**:
   - The main route (`/`) displays the task form and list
   - The `/add-task` route handles adding new tasks
   - The `/toggle-task/<task_id>` route handles marking tasks as complete or incomplete

5. **Bootstrap Integration**: We use Bootstrap classes for styling and responsive layout.

6. **Custom Styling**: We add custom CSS to enhance the appearance of our application.

## Extension Ideas

Here are some ways you could extend this application:

1. **Persistent Storage**: Replace the in-memory task list with a database (SQLite, PostgreSQL, etc.) using SQLAlchemy.

2. **Task Categories**: Add the ability to categorize tasks and filter by category.

3. **Due Dates**: Add due dates to tasks and sort by due date.

4. **User Authentication**: Add user accounts so each user can have their own task list.

5. **HTMX Integration**: Use HTMX to make the application more interactive without full page reloads:
   - Add tasks without refreshing the page
   - Toggle task completion with a simple click
   - Filter tasks dynamically

6. **Task Search**: Add a search functionality to find specific tasks.

7. **Task Priority**: Add priority levels to tasks and sort by priority.

8. **Task Notes**: Allow users to add detailed notes to tasks.

9. **Task Deletion**: Add the ability to delete tasks.

10. **Responsive Design Improvements**: Enhance the mobile experience with more responsive design elements.

## Conclusion

In this tutorial, we've built a simple but functional task management application using Viol. We've demonstrated how to:

- Set up a Flask application with Viol integration
- Create reusable UI components
- Handle form submissions and actions
- Style the application using Bootstrap and custom CSS

Viol's component-based approach makes it easy to build web applications in a Pythonic way, without having to write HTML templates directly. The integration with Bootstrap provides a solid foundation for creating responsive, attractive UIs.

By extending this application with some of the ideas mentioned above, you can create a more powerful and feature-rich task management tool tailored to your specific needs.