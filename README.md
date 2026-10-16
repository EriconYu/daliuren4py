# daliuren4py

Python 原生大六壬排盘 SDK，历法使用 `lunar-python`，三传使用包内规则表。运行时不依赖 Node.js 或其他语言。

```python
from daliuren4py import calculate, canonical

input_data = {
    "date": "2026-09-04", "hour": 18, "minute": 0,
    "timezone": "Asia/Shanghai",
}
chart = calculate(input_data)
portable = canonical(input_data)
```

`calculate` 返回完整结构化盘面，`canonical` 返回规范 JSON。当前算法版本为 `daliuren-shizhan-v1`。
