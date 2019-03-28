from secretary import Renderer
import os, tempfile

from django.http import HttpResponse

def format_date(value):
    try:
        return value.strftime('%d/%m/%Y')
    except:
        return ""

def format_datetime(value):
    try:
        return value.strftime('%d/%m/%Y %Hh%i')
    except:
        return ""

class ODTGenerator:
    def __init__(self, filepath, filename):
        self.template = os.path.dirname(__file__) + '/templates/' + filepath
        self.filename = filename

    def render(self, context):
        engine = Renderer()
        engine.environment.filters['format_date'] = format_date
        engine.environment.filters['format_datetime'] = format_datetime
        result = engine.render(self.template, **context)

        response = HttpResponse(content_type='application/vnd.oasis.opendocument.text; charset=UTF-8')
        response['Content-Disposition'] = 'inline; filename=' + self.filename
        with tempfile.NamedTemporaryFile() as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response