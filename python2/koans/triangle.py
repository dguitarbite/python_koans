#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.


# triangle(a, b, c) analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#
def triangle(a, b, c):

    # Check if the triangle is valid.
    if a < 1 or b < 1 or c < 1:
        raise TriangleError, "Invalid triangle"

    s1, s2, s3 = sorted([a, b, c])

    # Check if the triangle is valid.
    if s1 + s2 <= s3:
        raise TriangleError, "Invalid triangle"

    no_ueq_sides = len(set([a, b, c]))
    return ["equilateral", "isosceles", "scalene"][no_ueq_sides - 1]


# Error class used in part 2.  No need to change this code.
class TriangleError(StandardError):
    pass
