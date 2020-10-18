#
# syntaxhighlighting.py
# PyText3 Text Editor
#
# Created by Kaleb Rosborough on 12/3/2018
# Copyright © Shock9616 2018 All rights reserved
#

from pygments import lex
from pygments.lexers import PythonLexer

def HighlightSyntax(text_widget, theme, language):
    if theme == "monokai":
        if language == "C++":
            pass
        elif language == "HTML":
            pass
        elif language == "Java":
            pass
        elif language == "Javascript":
            pass
        elif language == "Plain Text":
            pass
        elif language == "Python":
            keywords = [
                "False",
                "None",
                "True",
                "and",
                "as",
                "assert",
                "break",
                "class",
                "continue",
                "def",
                "del",
                "elif",
                "else",
                "except",
                "finally",
                "for",
                "from",
                "global",
                "if",
                "import",
                "in",
                "is",
                "lambda",
                "nonlocal",
                "not",
                "or",
                "pass",
                "raise",
                "return",
                "try",
                "while",
                "with",
                "yield"
            ]

            syntax_types = [
                keywords
            ]

            textPad.mark_set("range_start", "1.0")
            data = textPad.get("1.0", "end-1c")
            for token, content in lex(data, PythonLexer()):
                textPad.mark_set("range_end", "range_start + %dc" % len(content))
                textPad.tag_add(str(token), "range_start", "range_end")
                textPad.mark_set("range_start", "range_end")

        elif language == "Swift":
            pass
        else:
            print("That is not a supported language")
