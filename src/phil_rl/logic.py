"""A bounded, function-free first-order language. Model text is never executable code."""

import re
import uuid
from dataclasses import dataclass

import z3

from phil_rl.schema import Formalization, Reconstruction, Symbol

OPS = {"not", "and", "or", "implies", "iff", "forall", "exists", "eq"}
NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,63}\Z")


@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()


def parse(text: str) -> Expr:
    if len(text) > 20000:
        raise ValueError("Formula is too long.")
    tokens = re.findall(r"\(|\)|[^\s()]+", text)
    if len(tokens) > 2048:
        raise ValueError("Formula has too many tokens.")
    position = 0

    def read(depth: int) -> Expr:
        nonlocal position
        if depth > 64 or position >= len(tokens):
            raise ValueError("Incomplete or excessively nested formula.")
        token = tokens[position]
        position += 1
        if token == "(":
            if position >= len(tokens) or not NAME.fullmatch(tokens[position]):
                raise ValueError("Expected operator or predicate after '('.")
            op = tokens[position]
            position += 1
            args = []
            while position < len(tokens) and tokens[position] != ")":
                args.append(read(depth + 1))
            if position >= len(tokens):
                raise ValueError("Missing ')'.")
            position += 1
            if not args:
                raise ValueError("Zero-arity propositions must be bare names.")
            return Expr(op, tuple(args))
        if not NAME.fullmatch(token):
            raise ValueError(f"Invalid token: {token!r}.")
        return Expr(token)

    expression = read(0)
    if position != len(tokens):
        raise ValueError("Trailing tokens after formula.")
    return expression


def validate_expr(expr: Expr, symbols: dict[str, Symbol], logic: str, bound=frozenset()):
    def term(value):
        if value.args or not (
            value.op in bound or (value.op in symbols and symbols[value.op].kind == "constant")
        ):
            raise ValueError(f"Unbound or invalid individual term: {value.op}.")

    op, args = expr.op, expr.args
    if op in {"true", "false"} and not args:
        return
    if op in {"not", "and", "or", "implies", "iff"}:
        arity = 1 if op == "not" else 2
        if len(args) != arity:
            raise ValueError(f"{op} expects {arity} arguments.")
        for arg in args:
            validate_expr(arg, symbols, logic, bound)
        return
    if op in {"forall", "exists"}:
        if logic != "classical_first_order" or len(args) != 2 or args[0].args:
            raise ValueError("Quantifiers require FOL and a variable followed by a formula.")
        variable = args[0].op
        if (
            variable in symbols
            or variable in OPS
            or variable in {"true", "false"}
            or variable in bound
        ):
            raise ValueError("Bound variable shadows another name.")
        validate_expr(args[1], symbols, logic, bound | {variable})
        return
    if op == "eq":
        if logic != "classical_first_order" or len(args) != 2:
            raise ValueError("Equality requires FOL and two individual terms.")
        for arg in args:
            term(arg)
        return
    symbol = symbols.get(op)
    if symbol is None or symbol.kind == "constant":
        raise ValueError(f"Undeclared proposition or predicate: {op}.")
    if len(args) != symbol.arity:
        raise ValueError(f"Arity mismatch for {op}.")
    for arg in args:
        term(arg)


def validate_formalization(reconstruction: Reconstruction, formalization: Formalization):
    names = [s.name for s in formalization.symbols]
    ids = [t.claim_id for t in formalization.translations]
    if len(names) != len(set(names)):
        raise ValueError("Symbol names must be unique.")
    if len(ids) != len(set(ids)) or set(ids) != {c.id for c in reconstruction.claims}:
        raise ValueError("Translate each frozen claim exactly once; do not add or remove claims.")
    if formalization.logic == "classical_propositional":
        if any(s.kind != "proposition" for s in formalization.symbols):
            raise ValueError("Propositional logic permits only proposition symbols.")
    if formalization.logic == "unsupported":
        if any(t.formula is not None for t in formalization.translations):
            raise ValueError("Unsupported logic must abstain from formalization.")
        return
    symbols = {s.name: s for s in formalization.symbols}
    for translation in formalization.translations:
        if translation.formula is not None:
            validate_expr(parse(translation.formula), symbols, formalization.logic)


class Z3Compiler:
    def __init__(self, formalization: Formalization, domain_size: int | None = None):
        self.grounding_budget = 20000
        self.elements = None
        if domain_size is None:
            self.domain = z3.DeclareSort("Domain")
        else:
            if not 1 <= domain_size <= 4:
                raise ValueError("Finite model search supports domains of size 1 through 4.")
            name = "FiniteDomain_" + uuid.uuid4().hex
            self.domain, self.elements = z3.EnumSort(
                name, [f"{name}_{i}" for i in range(domain_size)]
            )
        self.symbols = {}
        for symbol in formalization.symbols:
            if symbol.kind == "proposition":
                value = z3.Bool(symbol.name)
            elif symbol.kind == "constant":
                value = z3.Const(symbol.name, self.domain)
            else:
                value = z3.Function(symbol.name, *([self.domain] * symbol.arity), z3.BoolSort())
            self.symbols[symbol.name] = value

    def compile(self, expr: Expr, bound=None):
        self.grounding_budget -= 1
        if self.grounding_budget < 0:
            raise ValueError("Formula compilation exceeded the grounding budget.")
        bound = {} if bound is None else bound
        op, args = expr.op, expr.args
        if op in {"true", "false"}:
            return z3.BoolVal(op == "true")
        if op in {"forall", "exists"}:
            if self.elements is not None:
                instances = [self.compile(args[1], {**bound, args[0].op: v}) for v in self.elements]
                return (z3.And if op == "forall" else z3.Or)(*instances)
            var = z3.FreshConst(self.domain, prefix="bound_" + args[0].op)
            body = self.compile(args[1], {**bound, args[0].op: var})
            return (z3.ForAll if op == "forall" else z3.Exists)([var], body)
        if op == "eq":
            return self._term(args[0], bound) == self._term(args[1], bound)
        operators = {
            "not": z3.Not,
            "and": z3.And,
            "or": z3.Or,
            "implies": z3.Implies,
            "iff": lambda a, b: a == b,
        }
        if op in operators:
            return operators[op](*(self.compile(arg, bound) for arg in args))
        value = self.symbols[op]
        return value(*(self._term(a, bound) for a in args)) if args else value

    def _term(self, expr, bound):
        return bound[expr.op] if expr.op in bound else self.symbols[expr.op]


def to_lean(expr: Expr) -> str:
    """Prefix identifiers so user/model symbol names cannot inject Lean declarations."""
    op, args = expr.op, expr.args
    if op in {"true", "false"}:
        return op.title()
    if op in {"forall", "exists"}:
        quantifier = "∀" if op == "forall" else "∃"
        return f"({quantifier} s_{args[0].op} : Domain, {to_lean(args[1])})"
    if op == "not":
        return f"(¬ {to_lean(args[0])})"
    operators = {"and": "∧", "or": "∨", "implies": "→", "iff": "↔", "eq": "="}
    if op in operators:
        return f"({to_lean(args[0])} {operators[op]} {to_lean(args[1])})"
    if args:
        return "(" + " ".join(["s_" + op, *(to_lean(a) for a in args)]) + ")"
    return "s_" + op
