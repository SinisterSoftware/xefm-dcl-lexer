from pygments import lex
from pygments.token import Keyword, Name
from dcl_lexer.logic import DclLexer

def test_dcl_lexer_recognizes_tile_types_and_names():
    tokens = list(lex("mydialog : dialog { ok_cancel; }", DclLexer()))
    assert any(kind in Keyword and value == "dialog" for kind, value in tokens)
    assert any(kind in Name.Class and value == "mydialog" for kind, value in tokens)
