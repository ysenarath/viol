from flask import request

from viol.bootstrap.breadcrumb import Breadcrumb


def simple_breadcrumb() -> Breadcrumb:
    """Create a simple breadcrumb navigation."""
    request_path = request.path.strip("/").split("/")
    return Breadcrumb(
        location=[
            ("Home", "/"),
            *[
                (part.capitalize(), f"/{'/'.join(request_path[: i + 1])}")
                for i, part in enumerate(request_path)
                if part
            ],
        ],
        attrs={"class": ["my-3"]},
    )
