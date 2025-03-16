Contributing to Documentation
==========================

This guide explains how to maintain and update the viol documentation.

Setting Up Documentation Environment
--------------------------------

1. Install development dependencies:

   .. code-block:: bash

       uv add --dev sphinx pydata-sphinx-theme sphinx-autodoc-typehints myst-parser

2. The documentation source files are located in ``docs/source/``.

Directory Structure
----------------

.. code-block:: text

    docs/
    ├── source/          # Documentation source files
    │   ├── api/         # API documentation
    │   │   ├── bootstrap/   # Bootstrap components
    │   │   ├── html/       # HTML elements
    │   │   ├── core/       # Core functionality
    │   │   └── utils/      # Utilities
    │   ├── examples/   # Example documentation
    │   ├── conf.py     # Sphinx configuration
    │   └── index.rst   # Main documentation page
    ├── Makefile        # Build automation
    └── build/          # Generated documentation

Adding New Documentation
---------------------

1. **API Documentation**
   
   - Add new RST files in the appropriate subdirectory under ``api/``
   - Update the corresponding ``index.rst`` to include the new file
   - Example for a new bootstrap component:

   .. code-block:: rst

       Component Name
       =============

       .. automodule:: viol.bootstrap.component
          :members:
          :undoc-members:
          :show-inheritance:

2. **Examples**
   
   - Add new RST files in ``examples/``
   - Include code snippets with explanations
   - Update ``index.rst`` to list the new example

3. **General Documentation**
   
   - Create new RST files in ``source/``
   - Add them to the toctree in ``index.rst``

Building Documentation
-------------------

1. Navigate to the docs directory:

   .. code-block:: bash

       cd docs

2. Build HTML documentation:

   .. code-block:: bash

       make html

3. View the results:

   .. code-block:: bash

       open build/html/index.html

4. Clean build files (if needed):

   .. code-block:: bash

       make clean

Writing Style Guide
----------------

1. **Headers**
   
   - Use appropriate header levels
   - Keep consistent header markers:
     - ``=`` for top-level headers
     - ``-`` for second-level headers
     - ``^`` for third-level headers

2. **Code Examples**
   
   - Use ``.. code-block:: python`` for Python code
   - Use ``.. code-block:: bash`` for shell commands
   - Include doctest directives where appropriate

3. **Cross-References**
   
   - Use ``:ref:`` for internal references
   - Use ``:class:``, ``:meth:``, etc. for Python objects
   - Link to external documentation when relevant

4. **Docstrings**
   
   - Follow Google style docstrings
   - Include type hints
   - Document parameters, returns, and exceptions

Common Tasks
----------

1. **Adding a New Module**

   .. code-block:: bash

       # Create module documentation file
       touch docs/source/api/new_module.rst
       
       # Add to index.rst toctree
       # .. toctree::
       #    :maxdepth: 2
       #    api/new_module

2. **Updating API Documentation**

   - After adding new functions/classes, rebuild docs
   - Check autodoc output for completeness
   - Add examples where helpful

3. **Adding Examples**

   - Create new example file in examples/
   - Include working code snippets
   - Explain key concepts
   - Add to examples section in index.rst

Tips and Best Practices
--------------------

1. **Regular Updates**
   
   - Update docs when adding new features
   - Keep examples current with API changes
   - Review and update existing docs periodically

2. **Quality Checks**
   
   - Build docs with warnings as errors:
     ``make html SPHINXOPTS="-W"``
   - Check all internal links
   - Verify code examples work
   - Review rendered HTML

3. **Version Control**
   
   - Commit documentation changes with related code
   - Include meaningful commit messages
   - Review docs before releasing new versions