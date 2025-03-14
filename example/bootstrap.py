from viol.bootstrap.accordion import (
    Accordion,
    AccordionBody,
    AccordionButton,
    AccordionCollapse,
    AccordionHeader,
    AccordionItem,
)


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
                            "Lorem ipsum dolor sit amet, consectetur adipiscing"
                            " elit. Integer nec odio. Praesent libero. Sed cursus"
                            " ante dapibus diam. Sed nisi. Nulla quis sem at nibh"
                            " elementum imperdiet. Duis sagittis ipsum. Praesent"
                            " mauris. Fusce nec tellus sed augue semper porta."
                            " Mauris massa. Vestibulum lacinia arcu eget nulla."
                            " Class aptent taciti sociosqu ad litora torquent per"
                            " conubia nostra, per inceptos himenaeos. Curabitur"
                            " sodales ligula in libero.",
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
                            "Lorem ipsum dolor sit amet, consectetur adipiscing"
                            " elit. Integer nec odio. Praesent libero. Sed cursus"
                            " ante dapibus diam. Sed nisi. Nulla quis sem at nibh"
                            " elementum imperdiet. Duis sagittis ipsum. Praesent"
                            " mauris. Fusce nec tellus sed augue semper porta."
                            " Mauris massa. Vestibulum lacinia arcu eget nulla."
                            " Class aptent taciti sociosqu ad litora torquent per"
                            " conubia nostra, per inceptos himenaeos. Curabitur"
                            " sodales ligula in libero.",
                        ),
                        id="sample-accordion-item-2",
                    ),
                ],
            ),
        ],
        id="sample-accordion",
    )
