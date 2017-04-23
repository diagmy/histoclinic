#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "front.settings")

    from django.core.management import execute_from_command_line
    # print(sys.argv)
    a = sys.argv
    l = len(a)
    if l < 2:
    	a.append('runserver')
    print(a)
    execute_from_command_line(a)
