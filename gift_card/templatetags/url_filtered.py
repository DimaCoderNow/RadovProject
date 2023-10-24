from django import template


register = template.Library()


@register.simple_tag
def get_filtered_url(value, field_name, urlencode):
    url = f'?{field_name}={value}'
    querystring = urlencode.split('&')
    if len(querystring) > 1:
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = "&".join(filtered_querystring)
        url = f'{url}&{encoded_querystring}'
    return url
