from django import template

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
