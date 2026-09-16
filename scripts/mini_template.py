#!/usr/bin/env python3
"""
mini_template.py — 极简模板引擎（v2.8.1）

零依赖，支持：
  1. {{变量}} 替换（支持点路径 {{a.b}}、{{this}}、循环内字段）
  2. {{#each 列表}}...{{/each}} 循环（支持任意嵌套）

用法：
    from mini_template import render
    html = render(template_text, data)

示例（嵌套 each）：
    tpl = "{{#each 节}}<h2>{{标题}}</h2>{{#each 条目}}<p>{{meta}}</p>{{/each}}{{/each}}"
    data = {"节": [{"标题": "工作", "条目": [{"meta": "A"}]}]}
    → "<h2>工作</h2><p>A</p>"
"""

import re

_VAR_RE = re.compile(r"\{\{\s*([\w.]+)\s*\}\}")
_EACH_OPEN = re.compile(r"\{\{#each\s+([\w.]+)\s*\}\}")
_EACH_CLOSE = re.compile(r"\{\{/each\}\}")


def _resolve(obj, path: str):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, (list, tuple)) and part.isdigit():
            idx = int(part)
            cur = cur[idx] if idx < len(cur) else None
        else:
            return None
        if cur is None:
            return None
    return cur


def _find_each_end(text: str, start: int) -> int:
    """从 start 开始找与当前 each 匹配的 {{/each}}（跳过嵌套 each）。"""
    depth = 1
    pos = start
    while pos < len(text):
        m_open = _EACH_OPEN.search(text, pos)
        m_close = _EACH_CLOSE.search(text, pos)
        if m_close and (not m_open or m_close.start() < m_open.start()):
            depth -= 1
            if depth == 0:
                return m_close.start()
            pos = m_close.end()
        elif m_open:
            depth += 1
            pos = m_open.end()
        else:
            break
    return len(text)


def _render_vars(text: str, ctx: dict) -> str:
    def repl(m):
        val = _resolve(ctx, m.group(1))
        if val is None:
            return ""
        if isinstance(val, bool):
            return "true" if val else "false"
        return str(val)
    return _VAR_RE.sub(repl, text)


def render(template: str, data: dict) -> str:
    """递归渲染：支持嵌套 each。"""
    return _render_rec(template, data)


def _render_rec(text: str, ctx: dict) -> str:
    out = []
    pos = 0
    while pos < len(text):
        m = _EACH_OPEN.search(text, pos)
        if not m:
            out.append(_render_vars(text[pos:], ctx))
            break
        out.append(_render_vars(text[pos:m.start()], ctx))
        end = _find_each_end(text, m.end())
        block = text[m.end():end]
        items = _resolve(ctx, m.group(1)) or []
        for item in items:
            sub = dict(ctx)
            sub["this"] = item
            if isinstance(item, dict):
                sub.update(item)
            out.append(_render_rec(block, sub))
        pos = end + len("{{/each}}")
    return "".join(out)


if __name__ == "__main__":
    # 自测：嵌套 each
    tpl = ("<h1>{{姓名}}</h1>"
           "{{#each 节}}<h2>{{标题}}</h2>"
           "{{#each 条目}}<p>{{meta}}</p><ul>{{#each 行}}<li>{{this}}</li>{{/each}}</ul>{{/each}}"
           "{{/each}}")
    d = {"姓名": "张三", "节": [
        {"标题": "工作经历", "条目": [{"meta": "A公司", "行": ["x", "y"]}]},
        {"标题": "项目经历", "条目": [{"meta": "P1", "行": ["m"]}]},
    ]}
    print(render(tpl, d))
