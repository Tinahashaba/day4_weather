"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    exa weather <city>
    exa (-i | --interactive)
    exa (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --baud=<n>  Baudrate [default: 9600]
"""

import sys
import cmd
import requests
from docopt import docopt, DocoptExit


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class interact(cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
            + ' (type help for a list of commands.)'
    prompt = '(Enter city to get weather updates) '
    file = None

    @docopt_cmd
    def do_weather(self, arg):
        """Usage: weather <city>"""
        city = arg['<city>']
        if city is not None:
            result = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c23bdd3c920067eecb8bd0fa3ab4b6dc')
            if result.status_code == 200:
                states = result.json()
                print('Weather:')
                weather = states['weather']
                condition = weather[0]
                picture = condition['description']
                print(picture)
            else:
                print('HTTP ERROR %d.' % result.status_code)

        else:
            print('BAD USER NAME')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    interact().cmdloop()

print(opt)
