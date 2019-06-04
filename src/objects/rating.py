import re
from enum import Enum

import objects.route 

class RatingVariant(Enum):
  def __eq__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value == other_variant.value

  def __lt__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value < other_variant.value

  def __gt__(self, other_variant):
    assert isinstance(other_variant, self.__class__)
    return self.value > other_variant.value

class Rating(object):
  @staticmethod
  def from_string(rating_string, rating_type):
    if rating_type == objects.route.RouteType.Boulder:
      return VRating.from_string(rating_string)
    return YDSRating.from_string(rating_string)

  def __init__(self, grade, base, variant):
    self.grade = grade
    self.base = base
    self.variant = variant

  def __repr__(self):
    return "Rating<{}>".format(self.grade)

  def __eq__(self, other_rating):
    assert isinstance(other_rating, self.__class__) 
    return self.grade == ydsrating.grade

  def __lt__(self, other_rating):
    assert isinstance(other_rating, self.__class__) 
    return self.base < other_rating.base or \
      (self.base == other_rating.base and self.variant < other_rating.variant)
 
  def __gt__(self, other_rating):
    assert isinstance(other_rating, self.__class__) 
    return self.base > other_rating.base or \
      (self.base == other_rating.base and self.variant > other_rating.variant)
 

class YDSRating(Rating):
  REGEX = r"\b5\.([0-9]+)([abcd+-]?)(\b|$)"

  class Variant(RatingVariant):
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
          "a": YDSRating.Variant.a,
          "-": YDSRating.Variant.minus,
          "b": YDSRating.Variant.b,
          "c": YDSRating.Variant.c,
          "+": YDSRating.Variant.plus,
          "d": YDSRating.Variant.d
      }.get(variant, YDSRating.Variant.flat)

  @staticmethod
  def from_string(rating_string):
    match = re.search(YDSRating.REGEX, rating_string)
    if match:
      return YDSRating(
        match.group(0),
        int(match.group(1)),
        YDSRating.Variant.from_string(match.group(2))
      )
    return None

class VRating(Rating):
  REGEX = r"\bV([0-9]+)(-[0-9]*|\+)?(\b|$)"

  class Variant(RatingVariant):
    minus = 1
    flat = 2
    plus = 3
    border_plus_one = 4 

    @staticmethod
    def from_string(variant, base_grade):
      return {
          "-": VRating.Variant.minus,
          "+": VRating.Variant.plus,
          "-{}".format(base_grade + 1): VRating.Variant.border_plus_one
      }.get(variant, VRating.Variant.flat)

  @staticmethod
  def from_string(rating_string):
    match = re.search(VRating.REGEX, rating_string)
    if match:
      grade = match.group(0)
      base_grade = int(match.group(1))
      variant = VRating.Variant.from_string(match.group(2), base_grade)
      return VRating(grade, base_grade, variant)
    return None

  def __init__(self, grade, base, variant):
    self.grade = grade
    self.base = base
    self.variant = variant

  def base_grade(self):
    return "V{}".format(self.base)

