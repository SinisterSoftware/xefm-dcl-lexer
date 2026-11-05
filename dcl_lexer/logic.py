"""AutoCAD DCL の Pygments レクサー。config.py の LEXERS から参照する。"""
from pygments.lexer import RegexLexer, bygroups
from pygments.token import (Comment, Keyword, Name, Number, Operator,
                            Punctuation, String, Text)


class DclLexer(RegexLexer):
    name = "DCL"
    aliases = ["dcl"]
    filenames = ["*.dcl"]

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"//.*?$", Comment.Single),
            (r"/\*", Comment.Multiline, "comment"),
            # 新しいタイル定義名:  mydialog : dialog {
            (r"[A-Za-z_]\w*(?=\s*:)", Name.Class),
            # タイル種別:  : row {   : button {   : ok_cancel;
            (r"(:)(\s*)([A-Za-z_]\w*)",
             bygroups(Punctuation, Text, Keyword)),
            # 属性名:  label = ...
            (r"[A-Za-z_]\w*(?=\s*=)", Name.Builtin),
            (r"=", Operator, "value"),
            # 波括弧なしのタイル参照:  ok_cancel;  spacer;
            (r"[A-Za-z_]\w*(?=\s*;)", Keyword),
            (r"[{};]", Punctuation),
            (r".", Text),          # 取りこぼし防止（必須）
        ],
        "value": [
            (r"\s+", Text),
            (r"//.*?$", Comment.Single),
            (r"/\*", Comment.Multiline, "comment"),
            (r'"', String, "string"),
            (r"[+-]?\d+(\.\d+)?([eE][+-]?\d+)?", Number),
            (r"[A-Za-z_]\w*", Name.Constant),   # true / left / centered ...
            (r";", Punctuation, "#pop"),
            (r"\}", Punctuation, "#pop"),       # ; 忘れの保険
            (r".", Text),
        ],
        "string": [
            (r"\\.", String),
            (r'[^"\\\n]+', String),
            (r'"', String, "#pop"),
            (r"[\\\n]", Text, "#pop"),          # 閉じ忘れ対策
        ],
        "comment": [
            (r"[^*]+", Comment.Multiline),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"\*", Comment.Multiline),
        ],
    }

