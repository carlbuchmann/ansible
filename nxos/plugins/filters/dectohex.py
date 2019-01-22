#
# decimal to hex filter
#
from jinja2 import TemplateError

import re

class FilterModule(object):

  def dectohex(self,number):
    return hex(number)[2:]

  def filters(self):
    return {
      'dectohex' : self.dectohex,
    }