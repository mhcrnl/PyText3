#
# prefs.py
# PyText3 Text Editor
#
# Created by Kaleb Rosborough on 10/29/2018
# Copyright © Shock9616 2018 All rights reserved
#

"""
Contains global arrays and variables that are too
long to keep in the already crazy long main file
"""

LANGUAGES = [
    "C++",
    "HTML",
    "Java",
    "JavaScript",
    "Plain Text",
    "Python",
    "Swift"
]

THEMES = [
    "manni",
    "igor",
    "lovelace",
    "xcode",
    "vim",
    "autumn",
    "abap",
    "vs",
    "rrt",
    "native",
    "perldoc",
    "borland",
    "arduino",
    "tango",
    "emacs",
    "friendly",
    "monokai",
    "paraiso-dark",
    "murphy",
    "bw",
    "pastie",
    "algol_nu",
    "paraiso-light",
    "trac",
    "default",
    "algol",
    "fruity"
]

FONTS = [
    "Arial",
    "Helvetica",
    "Source Code Pro",
    "Verdana",
    "Trebuchet MS",
    "Georgia",
    "Times New Roman",
    "Courier"
]

PREVEIW_TEXT = ("#coding utf-8\n"
                "from random import shuffle\n"
                "\n"
                "def main():\n"
                "    '''Shuffle the entered name 10 times'''\n"
                "    name = input('Name: '\n"
                "    chars = list(name)\n"
                "    for i in range(10):\n"
                "        shuffle(chars)\n"
                "        print(''.join(chars))\n")

CREDITS_TEXT = ("\n Many thanks to the many sources that I used for this project!\n"
                "   - python.org\n"
                "   - stackoverflow.com\n"
                "   - pygments.org\n"
                "   - TheNewBoston (YouTube)\n"
                "   - Brian Oakley (Stack Overflow)\n"
                "   - DiogoTheCoder (YouTube)")
