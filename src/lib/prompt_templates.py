import re
from dataclasses import dataclass
from pathlib import Path


_PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
_SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_DEFAULT_PROMPT_ROOT = Path(__file__).resolve().parents[2] / "prompts"


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    text: str

    def render(self, **context):
        def replace(match):
            key = match.group(1)
            if key not in context:
                raise ValueError(f"Prompt template '{self.name}' is missing value for '{key}'")
            return str(context[key])

        return _PLACEHOLDER_PATTERN.sub(replace, self.text)


@dataclass(frozen=True)
class ChatPromptTemplate:
    name: str
    metadata: dict
    system: PromptTemplate
    user: PromptTemplate

    def render(self, **context):
        return RenderedChatPrompt(
            metadata=self.metadata,
            system=self.system.render(**context),
            user=self.user.render(**context),
        )


@dataclass(frozen=True)
class RenderedChatPrompt:
    metadata: dict
    system: str
    user: str

    @property
    def inference_config(self):
        config = {}
        if "temperature" in self.metadata:
            config["temperature"] = self.metadata["temperature"]
        if "maxTokens" in self.metadata:
            config["maxTokens"] = self.metadata["maxTokens"]
        return config


class PromptTemplateManager:
    def __init__(self, prompt_root=None):
        self.prompt_root = Path(prompt_root or _DEFAULT_PROMPT_ROOT).resolve()

    def render(self, template_name, **context):
        return self.load(template_name).render(**context)

    def render_chat(self, template_name, **context):
        return self.load_chat(template_name).render(**context)

    def load(self, template_name):
        template_path = self._resolve_template_path(template_name)
        if not template_path.exists():
            raise ValueError(f"Prompt template not found: {template_name}")
        return PromptTemplate(
            name=template_name,
            text=template_path.read_text(encoding="utf-8").strip(),
        )

    def load_chat(self, template_name):
        template_path = self._resolve_template_path(template_name)
        if not template_path.exists():
            raise ValueError(f"Prompt template not found: {template_name}")

        metadata, body = _split_front_matter(template_path.read_text(encoding="utf-8"))
        sections = _parse_markdown_sections(body)
        if "System" not in sections or "User" not in sections:
            raise ValueError(
                f"Prompt template '{template_name}' must include ## System and ## User sections"
            )

        return ChatPromptTemplate(
            name=template_name,
            metadata=metadata,
            system=PromptTemplate(name=f"{template_name}#System", text=sections["System"]),
            user=PromptTemplate(name=f"{template_name}#User", text=sections["User"]),
        )

    def _resolve_template_path(self, template_name):
        relative_path = Path(template_name)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Prompt template path must be relative to {self.prompt_root}")

        template_path = (self.prompt_root / relative_path).resolve()
        try:
            template_path.relative_to(self.prompt_root)
        except ValueError as exc:
            raise ValueError(f"Prompt template path must stay under {self.prompt_root}") from exc
        return template_path


def _split_front_matter(text):
    stripped = text.strip()
    if not stripped.startswith("---"):
        return {}, stripped

    parts = stripped.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Prompt template front matter is not closed")

    return _parse_front_matter(parts[1]), parts[2].strip()


def _parse_front_matter(text):
    metadata = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Invalid prompt metadata line: {line}")

        key, value = line.split(":", 1)
        metadata[key.strip()] = _parse_metadata_value(value.strip())
    return metadata


def _parse_metadata_value(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _parse_markdown_sections(text):
    matches = list(_SECTION_PATTERN.finditer(text))
    sections = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections
