from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ice_ai.agents.spec import AgentSpec


# ============================================================
# CV DATA MODELS
# ============================================================

@dataclass
class CVProfile:
    full_name: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None


@dataclass
class CVExperience:
    role: str
    company: str
    start: str
    end: Optional[str] = None
    description: Optional[str] = None


@dataclass
class CVEducation:
    degree: str
    institution: str
    year: Optional[str] = None


@dataclass
class CVDocument:
    """
    Struttura canonica CV ICE-AI.
    """
    profile: CVProfile
    experience: List[CVExperience]
    education: List[CVEducation]
    skills: Dict[str, List[str]]
    languages: List[str]
    extras: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile.__dict__,
            "experience": [e.__dict__ for e in self.experience],
            "education": [e.__dict__ for e in self.education],
            "skills": self.skills,
            "languages": self.languages,
            "extras": self.extras,
        }


# ============================================================
# CV AGENT
# ============================================================

class CVAgent:
    """
    CVAgent (ICE-AI)

    Responsabilità:
    - Parsing testo grezzo (umano / OCR / note)
    - Normalizzazione in schema CV
    - Arricchimento semantico (LLM-ready)
    - Rendering astratto (HTML / PDF demandato a layer esterno)

    NON:
    - non salva file
    - non genera PDF
    - non dipende da UI
    """

    # --------------------------------------------------------
    # SPEC ICE-AI
    # --------------------------------------------------------

    spec = AgentSpec(
        name="cv-agent",
        description="Generazione e normalizzazione CV strutturato.",
        domains={"cv", "documents"},
        is_executor=True,
        is_observer=True,
        capabilities={
            "cv.parse.raw",
            "cv.normalize",
            "cv.enrich",
            "cv.render.context",
        },
        ui_label="CV Builder",
        ui_group="Documents",
        experimental=True,
    )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def parse_raw(
        self,
        text: str,
        *,
        hints: Optional[Dict[str, Any]] = None,
    ) -> CVDocument:
        """
        Parsing deterministico base da testo grezzo.

        (LLM potrà migliorare questo step)
        """

        lines = [l.strip() for l in text.splitlines() if l.strip()]
        profile = CVProfile()
        experience: List[CVExperience] = []
        education: List[CVEducation] = []

        # Heuristic base minimale
        if lines:
            profile.full_name = lines[0]

        if len(lines) > 1:
            profile.title = lines[1]

        skills: Dict[str, List[str]] = {"core": [], "soft": []}
        languages: List[str] = []

        return CVDocument(
            profile=profile,
            experience=experience,
            education=education,
            skills=skills,
            languages=languages,
            extras={
                "raw_text": text,
                "hints": hints or {},
            },
        )

    # --------------------------------------------------------

    def normalize(self, cv: CVDocument) -> CVDocument:
        """
        Normalizza campi mancanti e struttura.
        """
        if not cv.profile.summary:
            cv.profile.summary = (
                f"Profilo professionale di {cv.profile.full_name or 'candidato'}."
            )

        for exp in cv.experience:
            if not exp.end:
                exp.end = "Present"

        return cv

    # --------------------------------------------------------

    def enrich(
        self,
        cv: CVDocument,
        *,
        suggestions: Optional[Dict[str, Any]] = None,
    ) -> CVDocument:
        """
        Punto di innesto LLM:
        - migliora summary
        - arricchisce skill
        - deduce soft skills
        """
        if suggestions:
            cv.extras["suggestions"] = suggestions

        return cv

    # --------------------------------------------------------

    def render_context(self, cv: CVDocument) -> Dict[str, Any]:
        """
        Produce un contesto pronto per rendering (HTML, PDF, UI).
        """
        return {
            "type": "cv",
            "schema": cv.to_dict(),
            "sections": [
                "profile",
                "experience",
                "education",
                "skills",
                "languages",
            ],
        }
