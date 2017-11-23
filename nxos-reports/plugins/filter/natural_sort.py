#
# natural_sort filter
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from jinja2 import TemplateError

import re

class FilterModule(object):

  def natural_sort(key):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

  def filters(self):
    return {
      'natural_sort' : self.natural_sort,
    }
