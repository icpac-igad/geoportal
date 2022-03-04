
from django import template
from django.core.cache import cache
import requests

register = template.Library()

@register.inclusion_tag(filename='icpac_apps.html')
def get_icpac_apps():

    apps = cache.get('icpac_apps')

    if apps is None:
        try:
            r = requests.get("https://www.icpac.net/api/v2/gis_apps/")
            r.raise_for_status()

            r_json = r.json()

            apps = r_json.get("items", [])
            cache.set("icpac_apps", apps, 86400) # cache for 24 hours

        except requests.exceptions.HTTPError:
            apps = None

    return {
        "apps": apps
    }
