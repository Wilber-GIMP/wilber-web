from django import template

register = template.Library()


@register.simple_tag
def asset_liked(asset, user):
    return asset.is_liked(user)
