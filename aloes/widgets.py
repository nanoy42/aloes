from django.forms.widgets import Input
from django.forms.utils import flatatt
from django.template.loader import get_template

class DatePicker(Input):
    def render(self, name, value, attrs=None):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)
        template = get_template('datepicker.html')
        return template.render({
            'name': name,
            'attrs': flat_attrs,
            'id': attrs['id']
        })
