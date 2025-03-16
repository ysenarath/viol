Accordion Example
================

This example demonstrates how to create a Bootstrap accordion using viol's Bootstrap components.

Components Overview
----------------

First, import the necessary accordion components:

.. code-block:: python

    from viol.bootstrap.accordion import (
        Accordion,
        AccordionBody,
        AccordionButton,
        AccordionCollapse,
        AccordionHeader,
        AccordionItem,
    )

Creating an Accordion
------------------

The example shows how to create an accordion with multiple collapsible items:

.. code-block:: python

    def sample_accordion() -> Accordion:
        return Accordion(
            [
                AccordionItem(
                    [
                        AccordionHeader(
                            AccordionButton("Accordion Item #1"),
                        ),
                        AccordionCollapse(
                            AccordionBody(
                                "Lorem ipsum dolor sit amet...",
                            ),
                            id="sample-accordion-item-1",
                        ),
                    ],
                ),
                AccordionItem(
                    [
                        AccordionHeader(
                            AccordionButton("Accordion Item #2"),
                        ),
                        AccordionCollapse(
                            AccordionBody(
                                "Lorem ipsum dolor sit amet...",
                            ),
                            id="sample-accordion-item-2",
                        ),
                    ],
                ),
            ],
            id="sample-accordion",
        )

Component Breakdown
----------------

1. **Accordion**
    * The main container component
    * Takes a unique ID for DOM identification
    * Contains multiple AccordionItem components

2. **AccordionItem**
    * Individual collapsible section
    * Contains a header and collapse section

3. **AccordionHeader**
    * Contains the clickable button
    * Toggles the visibility of associated content

4. **AccordionButton**
    * The clickable element that triggers collapse/expand
    * Contains the section title

5. **AccordionCollapse**
    * The collapsible container
    * Requires a unique ID for targeting
    * Contains the AccordionBody

6. **AccordionBody**
    * Contains the actual content
    * Shown/hidden when header is clicked

Features
-------

1. **Accessibility**
    * Proper ARIA attributes for screen readers
    * Keyboard navigation support

2. **Bootstrap Integration**
    * Uses Bootstrap's accordion classes
    * Follows Bootstrap's component structure

3. **Customization**
    * Each component can be styled individually
    * Content can be any valid HTML or viol components

4. **Interaction**
    * Click to expand/collapse sections
    * Multiple sections can be open simultaneously
