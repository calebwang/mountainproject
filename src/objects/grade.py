import re
from enum import Enum

import objects.route 

class GradeVariant(Enum):
  def __eq__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value == other_variant.value

  def __lt__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value < other_variant.value

  def __gt__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value > other_variant.value

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
    assert isinstance(other_grade, self.__class__) 
    return self.base < other_grade.base or \
      (self.base == other_grade.base and self.variant < other_grade.variant)
 
  def __gt__(self, other_grade):
    assert isinstance(other_grade, self.__class__) 
    return self.base > other_grade.base or \
      (self.base == other_grade.base and self.variant > other_grade.variant)
 

class YDSGrade(Grade):
  REGEX = r"\b5\.([0-9]+)([abcd+-]?)(\b|$)"
  _grades = {}

  class Variant(GradeVariant):
    a = 1
    minus = 1.5
    b = 2
    flat = 2.5
    c = 3
    plus = 3.5
    d = 4

    @staticmethod
    def from_string(variant):
      return {
          "a": YDSGrade.Variant.a,
          "-": YDSGrade.Variant.minus,
          "b": YDSGrade.Variant.b,
          "c": YDSGrade.Variant.c,
          "+": YDSGrade.Variant.plus,
          "d": YDSGrade.Variant.d
      }.get(variant, YDSGrade.Variant.flat)

  @staticmethod
  def from_string(grade_string):
    match = re.search(YDSGrade.REGEX, grade_string)
    if match:
      return YDSGrade._grades[match.group(0)]

for base_grade in range(0, 10):
  for variant in ["-", "", "+"]:
    grade = "5.{}{}".format(base_grade, variant)
    YDSGrade._grades[grade] = YDSGrade(grade, base_grade, YDSGrade.Variant.from_string(variant))
for base_grade in range(10, 16):
  for variant in ["a", "b", "c", "d", "-", "+", ""]:
    grade = "5.{}{}".format(base_grade, variant)
    YDSGrade._grades[grade] = YDSGrade(grade, base_grade, YDSGrade.Variant.from_string(variant))
      


class VGrade(Grade):
  REGEX = r"\bV([0-9]+)(-[0-9]*|\+)?(\b|$)"
  _grades = {}

  class Variant(GradeVariant):
    minus = 1
    flat = 2
    plus = 3
    border_plus_one = 4 

    @staticmethod
    def from_string(variant, base_grade):
      return {
          "-": VGrade.Variant.minus,
          "+": VGrade.Variant.plus,
          "-{}".format(base_grade + 1): VGrade.Variant.border_plus_one
      }.get(variant, VGrade.Variant.flat)


  @staticmethod
  def from_string(grade_string):
    match = re.search(VGrade.REGEX, grade_string)
    if match:
      return VGrade._grades[match.group(0)]
    return None

for base_grade in range(0, 17):
  for variant in ["-", "", "+", "-{}".format(base_grade + 1)]:
    grade = "V{}{}".format(base_grade, variant)
    VGrade._grades[grade] = VGrade(
      grade, int(base_grade), VGrade.Variant.from_string(variant, base_grade)
    )


