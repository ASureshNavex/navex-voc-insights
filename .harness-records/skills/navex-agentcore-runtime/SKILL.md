---
name: navex-agentcore-runtime
description: The Account Scoring Agent on Bedrock AgentCore - LangGraph graph layout, .j2 prompt templates with typed context, Pydantic v2 structured output, MCP tool ports, AgentCore Identity and Memory isolation. Use when working under services/account-scoring-agent, on a graph, node, prompt or explanation; read explanations.md beside it for a prompt or explanation change.
---

# AgentCore Runtime (LangGraph & Amazon Bedrock): Engineering Skill

When building, refactoring, or reviewing any AI agent running on **Amazon Bedrock AgentCore Runtime**, strictly separate graph orchestration, tool integrations, and externalized Jinja2 prompt templates.

---

## 1. Approved Stack & Quality Gate
- **Runtime & Orchestration:** Python 3.13, LangGraph, Amazon Bedrock AgentCore Runtime, AgentCore Identity, AgentCore Gateway, and AgentCore Memory
- **Models & Grounding:** Amazon Bedrock foundation models & Bedrock Knowledge Bases
- **Tool Protocol:** MCP Python SDK (`mcp`) for standardized tool and data-source connectors
- **Templating & Validation:** `Jinja2` (`StrictUndefined`) for all prompts; `Pydantic v2` for graph state, prompt context payloads, and structured LLM outputs
- **Tooling & CI Quality Gate:** `uv`, `ruff`, `mypy`, `pytest` + `pytest-asyncio`, `pip-audit`, and `trivy`

---

## 2. Standard AgentCore Folder Structure
Keep graph logic, state schemas, MCP tool clients, and Jinja2 prompt files strictly decoupled:

```text
<agent-service>/
|-- src/
|   |-- core/
|   |   |-- config.py             # Pydantic BaseSettings (Bedrock model IDs, KB IDs, timeouts)
|   |   |-- bedrock.py            # Bedrock runtime & structured-output model factories
|   |   |-- prompt_loader.py      # Centralized Jinja2 Environment loader (StrictUndefined)
|   |   |-- memory.py             # AgentCore Memory session/namespace isolation helpers
|   |   `-- telemetry.py          # OpenTelemetry traces, token usage metrics & structured logs
|   |-- graphs/
|   |   `-- <agent_name>/
|   |       |-- state.py          # Typed LangGraph state schema
|   |       |-- nodes.py          # Pure, testable async graph nodes
|   |       |-- edges.py          # Conditional routing functions
|   |       `-- graph.py          # Compiled StateGraph definition
|   |-- prompts/                  # ALL prompts live here as .j2 files (NEVER in .py files)
|   |   |-- shared/
|   |   |   |-- _persona.j2       # Shared system role & tone guidelines
|   |   |   `-- _grounding.j2     # Shared citation, anti-hallucination & safety rules
|   |   `-- <agent_name>/
|   |       |-- system.j2         # Agent-specific system instructions
|   |       `-- <step_name>.j2    # Task prompt with {{ placeholder }} variables
|   |-- schemas/
|   |   |-- prompt_contexts.py    # Pydantic v2 models validating Jinja2 template variables
|   |   `-- outputs.py            # Pydantic v2 models for Bedrock structured JSON outputs
|   |-- tools/                    # MCP Python SDK clients & AgentCore Gateway adapters
|   `-- entrypoint.py             # AgentCore Runtime invocation handler
|-- tests/
|   |-- test_prompts.py           # Automated tests rendering every .j2 template with mock models
|   `-- test_graphs.py            # Deterministic LangGraph node & routing tests
`-- pyproject.toml
```

---

## 3. Jinja2 Prompt Engineering Rules (Mandatory)
- **Zero Inline Prompts in Python:** Never hardcode multi-line prompt strings, f-strings, or `.format()` templates inside `.py` files. Every system and user prompt must reside in `src/prompts/` as a `.j2` template.
- **Strict Placeholder Validation (`StrictUndefined`):** Always render templates through a single `render_prompt()` helper configured with `undefined=jinja2.StrictUndefined`. If a placeholder variable (`{{ variable_name }}`) is missing or misspelled, rendering must fail fast before invoking Bedrock.
- **Typed Context Models:** Every `.j2` template must have a corresponding Pydantic v2 context model in `src/schemas/prompt_contexts.py`. Pass `context.model_dump()` into `template.render(...)` so dynamic values are type-checked and sanitized before substitution.
- **Composable Partials (`{% include %}`):** Extract repeated grounding instructions, output rules, and safety constraints into `src/prompts/shared/_*.j2` partials and compose them via `{% include 'shared/_grounding.j2' %}`.
- **Automated Template Tests:** Every new `.j2` file must have a unit test in `tests/test_prompts.py` verifying that it compiles cleanly and renders without `UndefinedError`.

```python
# Standard Pattern: src/core/prompt_loader.py
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import BaseModel

_PROMPTS_ROOT = Path(__file__).resolve().parent.parent / "prompts"

_env = Environment(
    loader=FileSystemLoader(str(_PROMPTS_ROOT)),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=False,
)


def render_prompt(template_name: str, context: BaseModel | None = None) -> str:
    template = _env.get_template(template_name)
    payload = context.model_dump() if context else {}
    return template.render(**payload)
```

---

## 4. LangGraph, MCP & AgentCore Security Rules
- **Pydantic v2 Structured Outputs:** Bind Bedrock models with `.with_structured_output(<OutputSchema>)` for every analytical, classification, or synthesis node so downstream databases and APIs receive guaranteed valid JSON.
- **MCP Tool Isolation:** Access external systems (databases, Knowledge Bases, classification engines) exclusively through typed MCP Python SDK clients or AgentCore Gateway tools, never embed raw SQL or vendor HTTP calls inside LangGraph nodes.
- **Evidence-Grounded Responses:** When querying Bedrock Knowledge Bases or feedback stores, pass retrieved chunk/record IDs into the Jinja2 template (`{% for doc in evidence %}[{{ doc.id }}] {{ doc.text }}{% endfor %}`) and require inline citations in the structured output.
- **AgentCore Identity & Memory Scoping:** Always scope AgentCore Identity tokens and AgentCore Memory namespaces to the caller's tenant/user/scope context (`OWN_BOOK`, `TEAM`, `REGION`, `ALL`) so memory or cached context never leaks across RBAC boundaries.
- **Bounded Graph Execution:** Configure explicit `recursion_limit`, node timeouts, and retry policies on Bedrock API calls to prevent runaway loops or hanging AgentCore sessions.
- **Local AWS SSO Testing:** Local agent execution and Bedrock invocations must use AWS CLI v2 named profiles (`AWS_PROFILE=navexdev`, `AWS_REGION=us-west-2`, `sso_session = navexsso`). Never commit static AWS keys.
