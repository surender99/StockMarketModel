"""Safe strategy rule expression evaluation — REQ-STRAT-CONFIG-001."""

from __future__ import annotations

import ast
import math
from typing import Any

import numpy as np
import pandas as pd

_ALLOWED_BINOPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
}
_ALLOWED_CMPOPS = {
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
}
_ALLOWED_BOOLOPS = {ast.And, ast.Or}
_ALLOWED_UNARYOPS = {ast.Not, ast.USub}


class ExpressionError(ValueError):
    """Invalid or unsafe strategy expression."""


def _validate_ast(node: ast.AST) -> None:
    if isinstance(node, ast.Expression):
        _validate_ast(node.body)
        return
    if isinstance(node, ast.BoolOp):
        if type(node.op) not in _ALLOWED_BOOLOPS:
            raise ExpressionError(f"unsupported boolean operator: {type(node.op).__name__}")
        for value in node.values:
            _validate_ast(value)
        return
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            raise ExpressionError(f"unsupported unary operator: {type(node.op).__name__}")
        _validate_ast(node.operand)
        return
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ExpressionError(f"unsupported binary operator: {type(node.op).__name__}")
        _validate_ast(node.left)
        _validate_ast(node.right)
        return
    if isinstance(node, ast.Compare):
        _validate_ast(node.left)
        for op, comparator in zip(node.ops, node.comparators, strict=True):
            if type(op) not in _ALLOWED_CMPOPS:
                raise ExpressionError(f"unsupported comparison: {type(op).__name__}")
            _validate_ast(comparator)
        return
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Attribute):
            raise ExpressionError("only attribute calls are allowed")
        if not isinstance(node.func.value, ast.Name):
            raise ExpressionError("shift calls must reference indicator names")
        if node.func.attr != "shift":
            raise ExpressionError(f"unsupported method: {node.func.attr}")
        if len(node.args) != 1 or node.keywords:
            raise ExpressionError("shift accepts exactly one positional argument")
        if not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, int):
            raise ExpressionError("shift argument must be an integer literal")
        if node.args[0].value < 0:
            raise ExpressionError("shift lag must be non-negative")
        return
    if isinstance(node, ast.Name):
        return
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return
    raise ExpressionError(f"unsupported expression node: {type(node).__name__}")


def _eval_node(node: ast.AST, env: dict[str, Any]) -> Any:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env)
    if isinstance(node, ast.BoolOp):
        values = [_eval_node(v, env) for v in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        return any(values)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, env)
        if isinstance(node.op, ast.Not):
            return not operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ExpressionError(f"unsupported unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env)
        right = _eval_node(node.right, env)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left / right
    if isinstance(node, ast.Compare):
        left = _eval_node(node.left, env)
        for op, comparator in zip(node.ops, node.comparators, strict=True):
            right = _eval_node(comparator, env)
            if isinstance(op, ast.Eq) and left != right:
                return False
            if isinstance(op, ast.NotEq) and left == right:
                return False
            if isinstance(op, ast.Lt) and not left < right:
                return False
            if isinstance(op, ast.LtE) and not left <= right:
                return False
            if isinstance(op, ast.Gt) and not left > right:
                return False
            if isinstance(op, ast.GtE) and not left >= right:
                return False
            left = right
        return True
    if isinstance(node, ast.Call):
        assert isinstance(node.func, ast.Attribute)
        assert isinstance(node.func.value, ast.Name)
        name = node.func.value.id
        lag = int(node.args[0].value)  # type: ignore[attr-defined]
        series = env[name]
        if not isinstance(series, pd.Series):
            msg = f"{name} is not a series in expression context"
            raise ExpressionError(msg)
        idx = env["__index__"]
        target = idx - lag
        if target < 0:
            return math.nan
        return series.iloc[target]
    if isinstance(node, ast.Name):
        value = env[node.id]
        if isinstance(value, pd.Series):
            idx = env["__index__"]
            return value.iloc[idx]
        return value
    if isinstance(node, ast.Constant):
        return node.value
    raise ExpressionError(f"cannot evaluate node: {type(node).__name__}")


def evaluate_condition_at_index(
    condition: str,
    frame: pd.DataFrame,
    indicator_columns: dict[str, str],
    index: int,
) -> bool:
    """Evaluate a strategy condition at a single bar index without lookahead."""
    tree = ast.parse(condition, mode="eval")
    _validate_ast(tree)
    env: dict[str, Any] = {"__index__": index}
    for indicator_id, column in indicator_columns.items():
        if column not in frame.columns:
            msg = f"missing indicator column '{column}' for '{indicator_id}'"
            raise ExpressionError(msg)
        env[indicator_id] = frame[column]
    if "volume" in frame.columns:
        env["volume"] = frame["volume"]
    if "close" in frame.columns:
        env["close"] = frame["close"]
    result = _eval_node(tree, env)
    if isinstance(result, (bool, np.bool_)):
        return bool(result)
    if isinstance(result, (int, float, np.floating)) and (math.isnan(result) or pd.isna(result)):
        return False
    return bool(result)
