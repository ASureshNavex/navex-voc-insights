from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from pydantic import BaseModel

_PROMPTS_ROOT = Path(__file__).resolve().parent.parent / "prompts"

_env = Environment(
    loader=FileSystemLoader(str(_PROMPTS_ROOT)),
    undefined=StrictUndefined,
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=False,
)


def render_prompt(template_name: str, context: BaseModel | None = None) -> str:
    template = _env.get_template(template_name)
    payload = context.model_dump() if context else {}
    return template.render(**payload)


def template_names() -> list[str]:
    return sorted(name for name in _env.list_templates(extensions=["j2"]))
