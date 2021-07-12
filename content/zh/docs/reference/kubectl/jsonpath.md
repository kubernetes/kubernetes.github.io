---
title: JSONPath 支持
content_type: concept
weight: 25
---
<!--
---
title: JSONPath Support
content_type: concept
weight: 25
---
-->

<!-- overview -->
<!--
Kubectl supports JSONPath template.
-->
Kubectl 支持 JSONPath 模板。


<!-- body -->

<!--
JSONPath template is composed of JSONPath expressions enclosed by curly braces {}.
Kubectl uses JSONPath expressions to filter on specific fields in the JSON object and format the output.
In addition to the original JSONPath template syntax, the following functions and syntax are valid:
-->
JSONPath 模板由 {} 包起来的 JSONPath 表达式组成。Kubectl 使用 JSONPath 表达式来过滤 JSON 对象中的特定字段并格式化输出。除了原始的 JSONPath 模板语法，以下函数和语法也是有效的:

<!--
1. Use double quotes to quote text inside JSONPath expressions.
2. Use the `range`, `end` operators to iterate lists.
3. Use negative slice indices to step backwards through a list. Negative indices do not "wrap around" a list and are valid as long as `-index + listLength >= 0`.
-->
1. 使用双引号将 JSONPath 表达式内的文本引起来。
2. 使用 `range`，`end` 运算符来迭代列表。
3. 使用负片索引后退列表。负索引不会“环绕”列表，并且只要 `-index + listLength> = 0` 就有效。

{{< note >}}
<!--
- The `$` operator is optional since the expression always starts from the root object by default.

- The result object is printed as its String() function.
-->
- `$` 运算符是可选的，因为默认情况下表达式总是从根对象开始。

- 结果对象将作为其 String() 函数输出。

{{< /note >}}

<!--
Given the JSON input:
-->
给定 JSON 输入:

```json
{
  "kind": "List",
  "items":[
    {
      "kind":"None",
      "metadata":{"name":"127.0.0.1"},
      "status":{
        "capacity":{"cpu":"4"},
        "addresses":[{"type": "LegacyHostIP", "address":"127.0.0.1"}]
      }
    },
    {
      "kind":"None",
      "metadata":{"name":"127.0.0.2"},
      "status":{
        "capacity":{"cpu":"8"},
        "addresses":[
          {"type": "LegacyHostIP", "address":"127.0.0.2"},
          {"type": "another", "address":"127.0.0.3"}
        ]
      }
    }
  ],
  "users":[
    {
      "name": "myself",
      "user": {}
    },
    {
      "name": "e2e",
      "user": {"username": "admin", "password": "secret"}
    }
  ]
}
```

<!--
Function            | Description               | Example                                                         | Result
--------------------|---------------------------|-----------------------------------------------------------------|------------------
`text`              | the plain text            | `kind is {.kind}`                                               | `kind is List`
`@`                 | the current object        | `{@}`                                                           | the same as input
`.` or `[]`         | child operator            | `{.kind}`, `{['kind']}` or `{['name\.type']}`                   | `List`
`..`                | recursive descent         | `{..name}`                                                      | `127.0.0.1 127.0.0.2 myself e2e`
`*`                 | wildcard. Get all objects | `{.items[*].metadata.name}`                                     | `[127.0.0.1 127.0.0.2]`
`[start:end :step]` | subscript operator        | `{.users[0].name}`                                              | `myself`
`[,]`               | union operator            | `{.items[*]['metadata.name', 'status.capacity']}`               | `127.0.0.1 127.0.0.2 map[cpu:4] map[cpu:8]`
`?()`               | filter                    | `{.users[?(@.name=="e2e")].user.password}`                      | `secret`
`range`, `end`      | iterate list              | `{range .items[*]}[{.metadata.name}, {.status.capacity}] {end}` | `[127.0.0.1, map[cpu:4]] [127.0.0.2, map[cpu:8]]`
`''`                | quote interpreted string  | `{range .items[*]}{.metadata.name}{'\t'}{end}`                  | `127.0.0.1      127.0.0.2`
-->
函数            | 描述               | 示例                                                         | 结果
--------------------|---------------------------|-----------------------------------------------------------------|------------------
`text`              | 纯文本            | `kind is {.kind}`                                               | `kind is List`
`@`                 | 当前对象        | `{@}`                                                           | 与输入相同
`.` or `[]`         | 子运算符            | `{.kind}`, `{['kind']}` or `{['name\.type']}`                    | `List`
`..`                | 递归下降         | `{..name}`                                                      | `127.0.0.1 127.0.0.2 myself e2e`
`*`                 | 通配符。获取所有对象 | `{.items[*].metadata.name}`                                     | `[127.0.0.1 127.0.0.2]`
`[start:end :step]` | 下标运算符        | `{.users[0].name}`                                              | `myself`
`[,]`               | 并集运算符            | `{.items[*]['metadata.name', 'status.capacity']}`               | `127.0.0.1 127.0.0.2 map[cpu:4] map[cpu:8]`
`?()`               | 过滤                    | `{.users[?(@.name=="e2e")].user.password}`                      | `secret`
`range`, `end`      | 迭代列表              | `{range .items[*]}[{.metadata.name}, {.status.capacity}] {end}` | `[127.0.0.1, map[cpu:4]] [127.0.0.2, map[cpu:8]]`
`''`                | 引用解释执行字符串  | `{range .items[*]}{.metadata.name}{'\t'}{end}`                  | `127.0.0.1      127.0.0.2`

<!--
Examples using `kubectl` and JSONPath expressions:
-->
使用 `kubectl` 和 JSONPath 表达式的示例:

```shell
kubectl get pods -o json
kubectl get pods -o=jsonpath='{@}'
kubectl get pods -o=jsonpath='{.items[0]}'
kubectl get pods -o=jsonpath='{.items[0].metadata.name}'
kubectl get pods -o=jsonpath="{.items[*]['metadata.name', 'status.capacity']}"
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
```

<!--
{{< note >}}
On Windows, you must _double_ quote any JSONPath template that contains spaces (not single quote as shown above for bash). This in turn means that you must use a single quote or escaped double quote around any literals in the template. For example:

```cmd
kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{'\t'}{.status.startTime}{'\n'}{end}"
kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{\"\t\"}{.status.startTime}{\"\n\"}{end}"
```
{{< /note >}}
-->
{{< note >}}
在 Windows 上，对于任何包含空格的 JSONPath 模板，您必须使用双引号（不是上面 bash 所示的单引号）。
反过来，这意味着您必须在模板中的所有文字周围使用单引号或转义的双引号。
例如:

```cmd
C:\> kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{'\t'}{.status.startTime}{'\n'}{end}"
C:\> kubectl get pods -o=jsonpath="{range .items[*]}{.metadata.name}{\"\t\"}{.status.startTime}{\"\n\"}{end}"
```
{{< /note >}}

<!--
JSONPath regular expressions are not supported. If you want to match using regular expressions, you can use a tool such as `jq`.

```shell
# kubectl does not support regular expressions for JSONpath output
# The following command does not work
kubectl get pods -o jsonpath='{.items[?(@.metadata.name=~/^test$/)].metadata.name}'

# The following command achieves the desired result
kubectl get pods -o json | jq -r '.items[] | select(.metadata.name | test("test-")).spec.containers[].image'
```
-->
{{< note >}}
不支持 JSONPath 正则表达式。如需使用正则表达式进行匹配操作，您可以使用如 `jq` 之类的工具。

```shell
# kubectl 的 JSONpath 输出不支持正则表达式
# 下面的命令不会生效
kubectl get pods -o jsonpath='{.items[?(@.metadata.name=~/^test$/)].metadata.name}'

# 下面的命令可以获得所需的结果
kubectl get pods -o json | jq -r '.items[] | select(.metadata.name | test("test-")).spec.containers[].image'
```
{{< /note >}}
