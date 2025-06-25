from lark import Lark, Transformer
import json

fol_grammar = r"""
    ?start: expr

    ?expr: implication
         | atom

    ?implication: atom "->" expr    -> implies
    ?atom: quantifier
         | predicate

    quantifier: "forall" VAR expr   -> forall_quant
    predicate: NAME "(" args ")"    -> predicate
    args: VAR ("," VAR)* | VAR

    VAR: /[a-zA-Z]/
    NAME: /[A-Za-z_][A-Za-z0-9_]*/

    %import common.WS
    %ignore WS
"""

class FOLTransformer(Transformer):
    def implies(self, items):
        return {"implies": {"if": items[0], "then": items[1]}}

    def forall_quant(self, items):
        return {"forall": {"var": str(items[0]), "body": items[1]}}

    def predicate(self, items):
        name = str(items[0])
        args = items[1] if len(items) > 1 else []
        return {"predicate": name, "args": args}

    def args(self, items):
        return [str(item) for item in items]

    def VAR(self, token):
        return str(token)

    def NAME(self, token):
        return str(token)

parser = Lark(fol_grammar, start='start', parser='lalr')
transformer = FOLTransformer()

expression = "forall x men(X) -> mortal(X)"
print(f"Parsing: {expression}")
tree = parser.parse(expression)
ast = transformer.transform(tree)
print(json.dumps(ast, indent=2))