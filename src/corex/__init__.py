# SPDX-FileCopyrightText: 2025-present Yasas Senarath <12231659+ysenarath@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
__version__ = "0.0.1"

# Import core classes for easy access
from .component import Component
from .app import CorexApp, create_app
from .components import (
    TextComponent,
    ButtonComponent,
    ContainerComponent,
    InputComponent,
    FormComponent,
    CardComponent,
    ListComponent,
)

# Define __all__ to control what gets imported with "from corex import *"
__all__ = [
    "Component",
    "CorexApp",
    "create_app",
    "TextComponent",
    "ButtonComponent",
    "ContainerComponent",
    "InputComponent",
    "FormComponent",
    "CardComponent",
    "ListComponent",
]
