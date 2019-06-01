"""Useful method for rendering and generating ODT documents."""
import os
import tempfile

from django.http import HttpResponse
from secretary import Renderer


def format_date(value):
    """Filter to display date correctly."""
    try:
        return value.strftime('%d/%m/%Y')
    except ValueError:  
        return ""

def format_datetime(value):
    """Filter to display date and time correctly."""
    try:
        return value.strftime('%d/%m/%Y %Hh%i')
    except ValueError:
        return ""

class ODTGenerator: # pylint: disable=too-few-public-methods
    """ODT renderer and generator."""
    def __init__(self, filepath, filename):
        self.template = os.path.dirname(__file__) + '/templates/' + filepath
        self.filename = filename

    def render(self, context):
        """Render the document using secretary."""
        engine = Renderer()
        engine.environment.filters['format_date'] = format_date
        engine.environment.filters['format_datetime'] = format_datetime
        result = engine.render(self.template, **context)
        response = HttpResponse(
            content_type='application/vnd.oasis.opendocument.text; charset=UTF-8'
        )
        response['Content-Disposition'] = 'inline; filename=' + self.filename
        with tempfile.NamedTemporaryFile() as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response
