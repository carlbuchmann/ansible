#
# strip spaces filter
#
from jinja2 import TemplateError

import re

class FilterModule(object):

  def strip_spaces(self,l):
    return(l.replace(" ", ""))

  def filters(self):
    return {
      'strip_spaces' : self.strip_spaces,
    }
