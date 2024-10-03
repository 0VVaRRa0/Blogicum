import textwrap

from django import template

register = template.Library()


@register.filter
def wrap_text(value, arg):
    """
    Фильтр разбивает текст на строки определенной длины
    и вставляет тег <br> в конце каждой строки.
    """
    wrapper = textwrap.TextWrapper(width=int(arg))
    word_list = wrapper.wrap(text=value)
    return '<br>'.join(word_list)
