from django import template
from django.contrib.contenttypes.models import ContentType
from campaign.models import MailTemplate


import re

register = template.Library()

@register.tag
def get_content_content_types_for_templates(parser, token):
    """
    Get all content ContentTypes associated to any templates.
    
    Syntax::
    
        {% get_content_content_types_for_templates as [var_name] %}
    
    Example usage::
    
        {% get_content_content_types_for_templates as ctlist %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires a var_name argument" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return ContentTypeNode(var_name)

class ContentTypeNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
    
    def render(self, context):
        templates = []
        for template in MailTemplate.objects.all():
            if (template.content_type):
                templates.append({
                    'id': template.id,
                    'content_type_id': template.content_type.id,
                    'content_type_app_label': template.content_type.app_label,
                    'content_type_model': template.content_type.model,
                })
        context[self.var_name] = templates
        return ''
