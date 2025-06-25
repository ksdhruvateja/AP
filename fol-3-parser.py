#modified to handle multiple statements and output JSON format

from lark import Lark, Transformer
import json

fol_grammar = r"""
    start: (expr NEWLINE?)+     -> multi

    ?expr: implication
         | conjunction
         | atom

    ?implication: expr "->" expr     -> implies
    ?conjunction: expr "and" expr    -> and_op

    ?atom: quantifier
         | predicate

    quantifier: "forall" VAR expr    -> forall_quant

    predicate: NAME "(" args ")"     -> predicate
    args: VAR ("," VAR)*

    VAR: /[a-zA-Z]/
    NAME: /[A-Za-z_][A-Za-z0-9_]*/

    %import common.WS
    %import common.NEWLINE
    %ignore WS
"""

class FOLTransformer(Transformer):
    def multi(self, statements):
        return {"statements": statements}

    def implies(self, items):
        return {"implies": {"if": items[0], "then": items[1]}}

    def and_op(self, items):
        return {"and": [items[0], items[1]]}

    def forall_quant(self, items):
        return {"forall": {"var": items[0], "body": items[1]}}

    def predicate(self, items):
        name = items[0]
        args = items[1:]
        return {"predicate": name, "args": args}

    def args(self, items):
        return items

    def VAR(self, token):
        return str(token)

    def NAME(self, token):
        return str(token)

#Parser and Transformer 
parser = Lark(fol_grammar, start='start', parser='lalr')
transformer = FOLTransformer()

expression = """
forall x men(X) -> mortal(X)
parent(P,X) and parent(P,Y) -> sibling(X,Y)
"""

print("Parsing input...")
tree = parser.parse(expression)
ast = transformer.transform(tree)
print(json.dumps(ast, indent=2))
