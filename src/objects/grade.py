import re
from enum import Enum

import objects.route 

class Grade(object):
  @staticmethod
  def from_string(grade_string, grade_type):
    if grade_type == objects.route.RouteType.Boulder:
      return VGrade.from_string(grade_string)
    return YDSGrade.from_string(grade_string)

  def __init__(self, grade, base, variant):
    self.grade = grade
    self.base = base
    self.variant = variant

  def __repr__(self):
    return "Grade<{}>".format(self.grade)

  def __eq__(self, other_grade):
    assert isinstance(other_grade, self.__class__) 
    return self.grade == other_grade.grade

  def __lt__(self, other_grade):
    variants = self.__class__.variants
    assert isinstance(other_grade, self.__class__) 
    return self.base < other_grade.base or \
      (self.base == other_grade.base and self.variant < other_grade.variant)
 
  def __gt__(self, other_grade):
    assert isinstance(other_grade, self.__class__) 
    return self.base > other_grade.base or \
      (self.base == other_grade.base and self.variant > other_grade.variant)

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


