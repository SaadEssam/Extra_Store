import pytest


def test_hello_world(test_fixture1):
  print("function_fixture1")
  assert test_fixture1 == 1


def test_hello_world2(test_fixture1):
  print("function_fixture2")
  assert test_fixture1 == 1
