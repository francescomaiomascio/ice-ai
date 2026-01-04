from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ice_ai.agents.spec import AgentSpec
from ice_ai.agents.capabilities import Capability


# ============================================================================
# AGENT
# ============================================================================

class KnowledgeSyncAgent:
    """
    KnowledgeSyncAgent
    ------------------

    Responsabilità:
    - esportare knowledge e timeline verso sistemi esterni
    - generare Markdown leggibile (Obsidian, vault, report)

    NON:
    - ragiona
    - modifica dati
    - interagisce con altri agenti
    """

    spec = AgentSpec(
        name="knowledge-sync-agent",
        description="Esporta knowledge e timeline in formati esterni (Markdown).",
        domains={"knowledge"},
        is_planner=False,
        is_executor=True,
        is_observer=False,
        is_system=False,
        capabilities={
            Capability.KNOWLEDGE_SYNC,
        },
        ui_label="Knowledge Export",
        ui_group="Persistence",
    )

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def export_markdown(
        self,
        *,
        title: str,
        sections: Dict[str, str],
        output_dir: str,
        filename: Optional[str] = None,
    ) -> str:
        """
        Esporta un documento Markdown strutturato.
        """

        if not title:
            raise ValueError("title mancante")

        if not sections:
            raise ValueError("sections vuote")

        os.makedirs(output_dir, exist_ok=True)

        safe_name = filename or title.replace(" ", "_").lower()
        path = os.path.join(output_dir, f"{safe_name}.md")

        md = self._build_markdown(title, sections)

        with open(path, "w", encoding="utf-8") as f:
            f.write(md)

        return path

    def export_timeline(
        self,
        *,
        title: str,
        events: List[Any],
        output_dir: str,
    ) -> str:
        """
        Esporta una timeline (es. HistorianAgent).
        """

        lines = []
        for ev in events:
            lines.append(
                f"- **{ev.timestamp}** "
                f"({ev.agent}) `{ev.type}` → {ev.message}"
            )

        sections = {
            "Timeline": "\n".join(lines)
        }

        return self.export_markdown(
            title=title,
            sections=sections,
            output_dir=output_dir,
        )

    def export_knowledge_items(
        self,
        *,
        title: str,
        items: List[Dict[str, Any]],
        output_dir: str,
    ) -> str:
        """
        Esporta item knowledge generici.
        """

        lines = []
        for it in items:
            kind = it.get("type", "item")
            content = it.get("content", "")
            lines.append(f"- **{kind}**: {content}")

        sections = {
            "Knowledge": "\n".join(lines)
        }

        return self.export_markdown(
            title=title,
            sections=sections,
            output_dir=output_dir,
        )

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _build_markdown(self, title: str, sections: Dict[str, str]) -> str:
        """
        Costruisce Markdown canonico ICE.
        """

        md: List[str] = [f"# {title}", ""]

        for name, content in sections.items():
            if not content:
                continue
            md.append(f"## {name}")
            md.append("")
            md.append(content.strip())
            md.append("")

        return "\n".join(md)
