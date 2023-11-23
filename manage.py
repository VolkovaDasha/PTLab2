#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tplab2.settings') # os - модуль для считывания переменных, хранящихся в словаре environ, где хранятся все переменные окружения
                                                                        #.setdefault (ключ, значение возвращаемое, если коюч не найден)
    try:
        from django.core.management import execute_from_command_line  #операция которая может вызвать исключение помещается в try
    except ImportError as exc:   #имя исключения импортэрор сохранено в перемнную экс 
        raise ImportError( # самостоятельный вызов исключения следующего содержания:
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
