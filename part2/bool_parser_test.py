# Module for testing bool expression parser.
# Reads a line at a time  from the stdin and prints the parsed expr to stdout.
#
# Olga Ohrimenko
# 02/2011

import sys
from bool_parser import bool_expr_ast

line = sys.stdin.readline()
while line != '':
  res = bool_expr_ast(line)
  a,b = res
  print a
  print b
  line = sys.stdin.readline()
