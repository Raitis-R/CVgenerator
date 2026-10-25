#!/usr/bin/env python
"""Django administrēšanas utilīta."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvgenerator.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nevar importēt Django. Vai esat aktivizējis conda vidi un "
            "izpildījis: pip install -r requirements.txt ?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
