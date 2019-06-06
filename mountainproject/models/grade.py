import re
from enum import Enum

import mountainproject.models.route

class Grade(object):
  @staticmethod
  def from_string(grade_string, grade_type=None):
    if grade_type == mountainproject.models.route.RouteType.Boulder:
      return VGrade.from_string(grade_string)
    elif grade_type in set([
        mountainproject.models.route.RouteType.Trad,
        mountainproject.models.route.RouteType.Sport, 
        mountainproject.models.route.RouteType.TR
    ]):
      return YDSGrade.from_string(grade_string)
    else:
      for grade_cls in [VGrade, YDSGrade]:
        grade_or_none = grade_cls.from_string(grade_string)
        if grade_or_none is not None:
          return grade_or_none
    return None

  def __init__(self, grade, base, variant):
    self._grade = grade
    self._base = base
    self._variant = variant

  def __str__(self):
    return self._grade

  def __repr__(self):
    return self._grade

  def __eq__(self, other_grade):
    if isinstance(other_grade, str):
      return self.__eq__(Grade.from_string(other_grade))
    if not isinstance(other_grade, self.__class__):
      return False

    return self._grade == other_grade._grade

  def __lt__(self, other_grade):
    if isinstance(other_grade, str):
      return self.__lt__(Grade.from_string(other_grade))
    if not isinstance(other_grade, self.__class__):
      return False

    return self._base < other_grade._base or \
      (self._base == other_grade._base and self._variant < other_grade._variant)
 
  def __gt__(self, other_grade):
    if isinstance(other_grade, str):
      return self.__gt__(Grade.from_string(other_grade))
    if not isinstance(other_grade, self.__class__):
      return False

    return self._base > other_grade._base or \
      (self._base == other_grade._base and self._variant > other_grade._variant)

  def base_grade(self):
    assert False
 

class YDSGrade(Grade):
  REGEX = r"\b5\.([0-9]+)([abcd+-]?)(\b|$)"
  _grades = {}
  _variants = ["", "-", "a", "a/b", "b", "b/c", "c", "c/d", "d", "+"]

  @staticmethod
  def from_string(grade_string):
    match = re.search(YDSGrade.REGEX, grade_string)
    if match:
      return YDSGrade._grades[match.group(0)]
    return None

  def base_grade(self):
    match = re.match(YDSGrade.REGEX, self.grade)
    return YDSGrade.from_string("5.{}".format(match.group(1)))

for base_grade in range(0, 10):
  for variant in ["-", "", "+"]:
    grade = "5.{}{}".format(base_grade, variant)
    variant_index = YDSGrade._variants.index(variant)
    YDSGrade._grades[grade] = YDSGrade(grade, base_grade, variant_index)
for base_grade in range(10, 16):
  for variant in YDSGrade._variants:
    grade = "5.{}{}".format(base_grade, variant)
    YDSGrade._grades[grade] = YDSGrade(grade, base_grade, YDSGrade._variants.index(variant))


class VGrade(Grade):
  REGEX = r"\bV([0-9]+)(-[0-9]*|\+)?(\b|$)"
  _grades = {}
  _variants = ["-", "", "+"]
  for base_grade in range(0, 17):
    _variants.append("-{}".format(base_grade + 1)) 

  @staticmethod
  def from_string(grade_string):
    match = re.search(VGrade.REGEX, grade_string)
    if match:
      return VGrade._grades[match.group(0)]
    return None

  def base_grade(self):
    match = re.match(VGrade.REGEX, self.grade)
    return VGrade.from_string("V{}".format(match.group(1)))

for base_grade in range(0, 17):
  for variant in ["-", "", "+", "-{}".format(base_grade + 1)]:
    grade = "V{}{}".format(base_grade, variant)
    variant_index = VGrade._variants.index(variant)
    VGrade._grades[grade] = VGrade(grade, int(base_grade), variant_index)


