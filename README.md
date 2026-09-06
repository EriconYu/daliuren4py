# daliuren4py

Python 大六壬排盘 SDK，包内自带经过版本锁定的排盘引擎。要求 Python 3.9+ 和 Node.js 20+。

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
