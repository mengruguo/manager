# -*- coding: utf-8 -*-

import os

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import StaticNode

register = template.Library()


class VersionFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        mtime = os.path.getmtime(os.path.join(settings.STATIC_ROOT, path.replace('/', os.sep))) * 1000
        return '%s?v=%ld' % (staticfiles_storage.url(path), mtime)


@register.tag(name='version')
def do_static(parser, token):
    return VersionFilesNode.handle_token(parser, token)
