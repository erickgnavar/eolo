from django import template
from django.conf import settings

register = template.Library()


@register.filter
def to_range(value):
    return range(1, value + 1)


class Path(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url


@register.filter
def path_to_list(path):
    if '?' in path:
        path = path.split('?')[0]
    urls = []
    path = path.split('/')
    n = len(path)
    for i in range(n):
        if not path[i] == '':
            url = Path(name=path[i], url='/'.join(path[:i + 1]))
            urls.append(url)
    return urls


@register.filter
def to_pipes(value):
    return '|' * len(value)


@register.filter
def pagination_range(page_obj):
    num_pages = page_obj.paginator.num_pages
    current = page_obj.number
    variation = settings.PAGE_LENGTH / 2
    min_value = current - variation
    max_value = current + variation
    if num_pages <= settings.PAGE_LENGTH:
        return range(1, num_pages)
    if min_value <= 0:
        return range(1, settings.PAGE_LENGTH)
    if max_value >= num_pages:
        return range(num_pages - settings.PAGE_LENGTH + 2, num_pages + 1)
    return range(min_value + 1, max_value)
