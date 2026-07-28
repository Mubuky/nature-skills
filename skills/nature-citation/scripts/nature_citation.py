#!/usr/bin/env python3
# Modified in the context-engineered edition; see repository NOTICE.
"""
Discover strict Nature/CNS-family candidates for manuscript claims.

Candidate discovery never produces insertion text or a reference-manager file.
Final ENW/RIS/RDF export requires a separately reviewed selection file with
semantic evidence locators.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape as xml_escape
from xml.sax.saxutils import quoteattr


CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = "codex-nature-citation/1.0 (mailto:unknown@example.com)"
EXPORT_FORMAT_CHOICES = ("enw", "ris", "zotero-rdf", "rdf")
DEFAULT_EXPORT_FORMAT = "enw"
SCREENED_SUPPORT_GRADES = {"strong", "partial", "background"}
SCREENED_EVIDENCE_LEVELS = {"abstract", "full_text", "publisher_page"}
ZOTERO_RDF_NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "z": "http://www.zotero.org/namespaces/export#",
    "dcterms": "http://purl.org/dc/terms/",
    "bib": "http://purl.org/net/biblio#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "prism": "http://prismstandard.org/namespaces/1.2/basic/",
}


NATURE_EXACT = {
    "Nature",
    "Nature Aging",
    "Nature Astronomy",
    "Nature Biomedical Engineering",
    "Nature Biotechnology",
    "Nature Cancer",
    "Nature Cardiovascular Research",
    "Nature Catalysis",
    "Nature Cell Biology",
    "Nature Chemical Biology",
    "Nature Chemical Engineering",
    "Nature Chemistry",
    "Nature Cities",
    "Nature Climate Change",
    "Nature Communications",
    "Nature Computational Science",
    "Nature Ecology & Evolution",
    "Nature Electronics",
    "Nature Energy",
    "Nature Food",
    "Nature Genetics",
    "Nature Geoscience",
    "Nature Health",
    "Nature Human Behaviour",
    "Nature Immunology",
    "Nature Machine Intelligence",
    "Nature Materials",
    "Nature Mechanical Engineering",
    "Nature Medicine",
    "Nature Mental Health",
    "Nature Metabolism",
    "Nature Methods",
    "Nature Microbiology",
    "Nature Nanotechnology",
    "Nature Neuroscience",
    "Nature Photonics",
    "Nature Physics",
    "Nature Plants",
    "Nature Sensors",
    "Nature Protocols",
    "Nature Reviews Cancer",
    "Nature Reviews Biodiversity",
    "Nature Reviews Bioengineering",
    "Nature Reviews Cardiology",
    "Nature Reviews Chemistry",
    "Nature Reviews Clean Technology",
    "Nature Reviews Clinical Oncology",
    "Nature Reviews Computing",
    "Nature Reviews Disease Primers",
    "Nature Reviews Drug Discovery",
    "Nature Reviews Earth & Environment",
    "Nature Reviews Electrical Engineering",
    "Nature Reviews Endocrinology",
    "Nature Reviews Gastroenterology & Hepatology",
    "Nature Reviews Genetics",
    "Nature Reviews Immunology",
    "Nature Reviews Materials",
    "Nature Reviews Methods Primers",
    "Nature Reviews Microbiology",
    "Nature Reviews Molecular Cell Biology",
    "Nature Reviews Nephrology",
    "Nature Reviews Neurology",
    "Nature Reviews Neuroscience",
    "Nature Reviews Physics",
    "Nature Reviews Psychology",
    "Nature Reviews Rheumatology",
    "Nature Reviews Urology",
    "Nature Structural & Molecular Biology",
    "Nature Sustainability",
    "Nature Synthesis",
    "Nature Water",
    "Nature Progress Brain Health",
    "Nature Progress Oncology",
    "Communications AI & Computing",
    "Communications Biology",
    "Communications Chemistry",
    "Communications Earth & Environment",
    "Communications Engineering",
    "Communications Health",
    "Communications Materials",
    "Communications Medicine",
    "Communications Physics",
    "Communications Psychology",
    "Communications Sustainability",
    "Scientific Data",
    "Scientific Reports",
    "Scientific Reviews",
}

# Exact snapshot from the official Nature Portfolio npj Series page, checked
# 2026-07-28. Unknown titles fail closed and should be verified on the current
# official portfolio page before being added.
NPJ_EXACT = {
    "npj 2D Materials and Applications",
    "npj Acoustics",
    "npj Advanced Manufacturing",
    "npj Aging",
    "npj Antimicrobials and Resistance",
    "npj Artificial Intelligence",
    "npj Autoimmunity",
    "npj Biodiversity",
    "npj Biocatalysis",
    "npj Biofilms and Microbiomes",
    "npj Biological Physics and Mechanics",
    "npj Biological Timing and Sleep",
    "npj Biomedical Innovations",
    "npj Biosensing",
    "npj Breast Cancer",
    "npj Cardiovascular Health",
    "npj Clean Air",
    "npj Clean Energy",
    "npj Clean Water",
    "npj Climate Action",
    "npj Climate and Atmospheric Science",
    "npj Complexity",
    "npj Computational Materials",
    "npj Dementia",
    "npj Digital Medicine",
    "npj Digital Public Health",
    "npj Digital Surgery",
    "npj Drug Discovery",
    "npj Emerging Contaminants",
    "npj Energy Materials",
    "npj Energy Systems and Resilience",
    "npj Entomology",
    "npj Environmental Social Sciences",
    "npj Exercise Medicine and Health",
    "npj Extreme Ecosystems",
    "npj Flexible Electronics",
    "npj Fungal Science",
    "npj Genomic Medicine",
    "npj Geoinformatics",
    "npj Gut and Liver",
    "npj Health Systems",
    "npj Heritage Science",
    "npj Hydrosphere",
    "npj Imaging",
    "npj Integrated Electronics",
    "npj Materials Degradation",
    "npj Materials Sustainability",
    "npj Mental Health Research",
    "npj Metabolic Health and Disease",
    "npj Metamaterials",
    "npj Microgravity",
    "npj Nanophotonics",
    "npj Natural Hazards",
    "npj Ocean Sustainability",
    "npj Pain",
    "npj Palaeoecosystems",
    "npj Parasitology",
    "npj Parkinson's Disease",
    "npj Power Electronics",
    "npj Precision Oncology",
    "npj Primary Care Respiratory Medicine",
    "npj Quantum Information",
    "npj Quantum Materials",
    "npj Regenerative Medicine",
    "npj Robotics",
    "npj Science of Food",
    "npj Science of Learning",
    "npj Science of Plants",
    "npj Self-Powered Electronics",
    "npj Soft Matter",
    "npj Soil Ecology",
    "npj Space Exploration",
    "npj Spintronics",
    "npj Structural Biology",
    "npj Sustainable Agriculture",
    "npj Sustainable Mobility and Transport",
    "npj Systems Biology and Applications",
    "npj Thermal Science and Engineering",
    "npj Toxicology",
    "npj Unconventional Computing",
    "npj Urban Sustainability",
    "npj Vaccines",
    "npj Veterinary Sciences",
    "npj Viruses",
    "npj Wireless Technology",
    "npj Women's Health",
}


SCIENCE_EXACT = {
    "Science",
    "Science Advances",
    "Science Immunology",
    "Science Robotics",
    "Science Signaling",
    "Science Translational Medicine",
}


CELL_EXACT = {
    "Cell",
    "Cancer Cell",
    "Cell Chemical Biology",
    "Cell Genomics",
    "Cell Host & Microbe",
    "Cell Metabolism",
    "Cell Reports",
    "Cell Reports Medicine",
    "Cell Reports Methods",
    "Cell Reports Physical Science",
    "Cell Stem Cell",
    "Cell Systems",
    "Chem",
    "Current Biology",
    "Developmental Cell",
    "Immunity",
    "Joule",
    "Med",
    "Molecular Cell",
    "Neuron",
    "One Earth",
    "Patterns",
    "Structure",
    "The Innovation",
}


CELL_TRENDS_EXACT = {
    "Trends in Biochemical Sciences",
    "Trends in Biotechnology",
    "Trends in Cancer",
    "Trends in Cell Biology",
    "Trends in Chemistry",
    "Trends in Cognitive Sciences",
    "Trends in Ecology & Evolution",
    "Trends in Endocrinology & Metabolism",
    "Trends in Genetics",
    "Trends in Immunology",
    "Trends in Microbiology",
    "Trends in Molecular Medicine",
    "Trends in Neurosciences",
    "Trends in Parasitology",
    "Trends in Pharmacological Sciences",
    "Trends in Plant Science",
}


FLAGSHIP = {"Nature", "Science", "Cell"}


@dataclass
class Segment:
    id: str
    text: str
    search_query: str
    order: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order": self.order,
            "text": self.text,
            "search_query": self.search_query,
        }


@dataclass
class Candidate:
    title: str
    journal: str
    family: str
    year: str
    y1: str
    doi: str
    url: str
    volume: str
    issue: str
    start_page: str
    end_page: str
    issn: str
    authors: list[str]
    abstract: str
    type: str
    score: float
    source_query: str

    @property
    def doi_url(self) -> str:
        return f"https://doi.org/{self.doi}" if self.doi else self.url

    @property
    def key(self) -> str:
        if self.doi:
            return self.doi.lower()
        return f"{self.title.lower()}|{self.journal.lower()}"

    @property
    def first_author(self) -> str:
        if not self.authors:
            return "Unknown author"
        return self.authors[0].split(",", 1)[0]

    @property
    def citation_marker(self) -> str:
        if self.year:
            return f"({self.first_author} et al., {self.year})"
        return f"({self.first_author} et al.)"

    @property
    def page_range(self) -> str:
        if self.start_page and self.end_page:
            return f"{self.start_page}-{self.end_page}"
        return self.start_page

    @property
    def identifier_url(self) -> str:
        return self.doi_url or self.url

    @property
    def article_resource(self) -> str:
        if self.identifier_url:
            return self.identifier_url
        return f"urn:candidate:{stable_hash(self.key or self.title or 'candidate')}"

    @property
    def journal_resource(self) -> str:
        return build_journal_resource(self)

    @property
    def zotero_citation_key(self) -> str:
        return build_zotero_citation_key(self)

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "journal": self.journal,
            "family": self.family,
            "year": self.year,
            "doi": self.doi,
            "url": self.url,
            "doi_url": self.doi_url,
            "volume": self.volume,
            "issue": self.issue,
            "start_page": self.start_page,
            "end_page": self.end_page,
            "issn": self.issn,
            "authors": self.authors,
            "abstract": self.abstract,
            "type": self.type,
            "score": self.score,
            "source_query": self.source_query,
            "support_grade": "metadata-only candidate",
            "screening_note": "Inspect abstract/publisher page before citing this paper as support.",
        }


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title or "").strip()


def stable_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")
    return slug or "item"


def normalize_export_format(value: str | None) -> str:
    if not value:
        return DEFAULT_EXPORT_FORMAT
    if value == "rdf":
        return "zotero-rdf"
    return value


def infer_export_format(output_path: Path | None) -> str:
    if output_path is None:
        return DEFAULT_EXPORT_FORMAT
    suffix = output_path.suffix.lower()
    if suffix == ".ris":
        return "ris"
    if suffix == ".rdf":
        return "zotero-rdf"
    if suffix == ".enw":
        return "enw"
    return DEFAULT_EXPORT_FORMAT


def export_filename(export_format: str, base: str = "references") -> str:
    if export_format == "ris":
        return f"{base}.ris"
    if export_format == "zotero-rdf":
        return f"{base}.rdf"
    return f"{base}.enw"


def slug_from_text(text: str, max_words: int = 6) -> str:
    """Derive a filename slug from the first meaningful words of manuscript text."""
    text = clean_text(text)
    text = re.sub(r"\[[^\]]+\]|\([A-Za-z]+ et al\.,? \d{4}\)", " ", text)
    words = re.findall(r"[A-Za-z0-9]+|[一-鿿]+", text)
    stopwords = {
        "the", "a", "an", "and", "or", "of", "to", "in", "for", "by", "with", "on", "at",
        "from", "is", "are", "was", "were", "be", "been", "being", "that", "this", "these",
        "those", "it", "its", "can", "may", "could", "not", "but", "as", "if", "into",
    }
    content = [w for w in words if w.lower() not in stopwords]
    slug = "-".join(w.lower() for w in content[:max_words])
    return slug or "references"


def export_label(export_format: str) -> str:
    if export_format == "ris":
        return "RIS"
    if export_format == "zotero-rdf":
        return "Zotero RDF"
    return "ENW"


def make_partial_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}.partial{path.suffix}")


def retry_with_backoff(action: Callable[[], Any], max_retries: int, base_delay: float = 0.5) -> Any:
    last_error: Exception | None = None
    retries = max(0, max_retries)
    for attempt in range(retries + 1):
        try:
            return action()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(base_delay * (2 ** attempt))
    if last_error is not None:
        raise last_error
    raise RuntimeError("retry_with_backoff() exited without returning or raising")


def resolve_batch_size(segment_count: int, args: argparse.Namespace) -> int:
    if getattr(args, "batch_size", 0) and args.batch_size > 0:
        return max(1, args.batch_size)
    if segment_count > 10:
        return 10
    return 0


def chunk_segments(segments: list[Segment], batch_size: int) -> list[list[Segment]]:
    if not segments:
        return []
    if batch_size <= 0 or batch_size >= len(segments):
        return [segments]
    return [segments[idx : idx + batch_size] for idx in range(0, len(segments), batch_size)]


def limit_segments(segments: list[Segment], max_segments: int) -> tuple[list[Segment], int]:
    if max_segments and max_segments > 0 and len(segments) > max_segments:
        return segments[:max_segments], len(segments) - max_segments
    return segments, 0


def zotero_date_value(item: Candidate) -> str:
    if item.y1:
        return item.y1.replace("/", "-")
    return item.year


def split_author_parts(name: str) -> tuple[str, str]:
    if "," in name:
        family, given = name.split(",", 1)
        return family.strip(), given.strip()
    parts = [part for part in name.split() if part]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[-1], " ".join(parts[:-1])


def build_journal_resource(item: Candidate) -> str:
    parts: list[str] = []
    if item.issn:
        parts.append(f"issn:{slugify(item.issn)}")
    elif item.journal:
        parts.append(f"title:{slugify(item.journal)}")
    else:
        parts.append(f"record:{stable_hash(item.key or item.title or 'journal')}")
    if item.volume:
        parts.append(f"vol:{slugify(item.volume)}")
    if item.issue:
        parts.append(f"issue:{slugify(item.issue)}")
    return "urn:" + ":".join(parts)


def build_zotero_citation_key(item: Candidate) -> str:
    first_author = slugify(item.first_author)
    title_words = re.findall(r"[A-Za-z0-9]+", item.title)[:3]
    title_part = "".join(word.capitalize() for word in title_words) or "Item"
    year = item.year or "n.d."
    return f"{first_author}{title_part}{year}"


def journal_family(journal: str) -> str | None:
    journal = normalize_title(journal)
    if not journal:
        return None
    if journal in NATURE_EXACT or journal in NPJ_EXACT:
        return "Nature Portfolio"
    if journal in SCIENCE_EXACT:
        return "Science family"
    if journal in CELL_EXACT or journal in CELL_TRENDS_EXACT:
        return "Cell Press"
    return None


def in_scope(journal: str, scope: str) -> bool:
    journal = normalize_title(journal)
    if not journal:
        return False
    if scope == "flagship":
        return journal in FLAGSHIP
    family = journal_family(journal)
    if scope == "nature":
        return family == "Nature Portfolio"
    if scope == "science":
        return family == "Science family"
    if scope == "cell":
        return family == "Cell Press"
    return family in {"Nature Portfolio", "Science family", "Cell Press"}


def first(values: list[Any] | None, default: str = "") -> str:
    if not values:
        return default
    value = values[0]
    if isinstance(value, str):
        return value
    return default


def date_parts(item: dict[str, Any]) -> list[int]:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            return parts[0]
    return []


def year_from_item(item: dict[str, Any]) -> str:
    parts = date_parts(item)
    return str(parts[0]) if parts else ""


def y1_from_item(item: dict[str, Any]) -> str:
    parts = date_parts(item)
    if not parts:
        return ""
    year = f"{parts[0]:04d}"
    month = f"{parts[1]:02d}" if len(parts) > 1 else "01"
    day = f"{parts[2]:02d}" if len(parts) > 2 else "01"
    return f"{year}/{month}/{day}"


def author_name(author: dict[str, Any]) -> str:
    family = author.get("family", "").strip()
    given = author.get("given", "").strip()
    if family and given:
        return f"{family}, {given}"
    return family or given or author.get("name", "").strip()


def pages(item: dict[str, Any]) -> tuple[str, str]:
    page = item.get("page", "") or item.get("article-number", "")
    if not page:
        return "", ""
    if "-" in page:
        start, end = page.split("-", 1)
        return start.strip(), end.strip()
    return page.strip(), ""


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ris_escape(text: str) -> str:
    return clean_text(text).replace("\n", " ").replace("\r", " ")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    pattern = r"(?<=[.!?。！？])\s+|(?<=[。！？])"
    return [part.strip() for part in re.split(pattern, text) if part.strip()]


def looks_like_heading(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) > 90:
        return False
    if stripped.endswith((".", "。", "!", "！", "?", "？")):
        return False
    words = stripped.split()
    if 0 < len(words) <= 8 and not any(char in stripped for char in ",;，；"):
        return True
    return False


def query_from_segment(text: str, max_words: int = 26) -> str:
    text = clean_text(text)
    text = re.sub(r"\[[^\]]+\]|\([A-Za-z]+ et al\.,? \d{4}\)", " ", text)
    words = re.findall(r"[A-Za-z0-9α-ωΑ-Ωβγδκλμνπρστυφχψω\-]+|[\u4e00-\u9fff]+", text)
    if not words:
        return text[:240]
    return " ".join(words[:max_words])


def fallback_queries_from_segment(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9α-ωΑ-Ωβγδκλμνπρστυφχψω\-]+|[\u4e00-\u9fff]+", clean_text(text))
    if not words:
        return []
    stopwords = {
        "the", "a", "an", "and", "or", "of", "to", "in", "for", "by", "with", "on", "at", "from",
        "reveals", "reveal", "revealed", "promote", "promotes", "promoted", "promoting",
        "suppress", "suppresses", "suppressing", "show", "shows", "showed", "indicate", "indicates",
        "indicated", "identify", "identifies", "identified", "can", "may", "could", "is", "are",
        "was", "were", "be", "been", "being", "that", "this", "these", "those",
    }
    content = [word for word in words if word.lower() not in stopwords]
    candidates: list[str] = []
    if len(content) >= 3:
        candidates.append(" ".join(content[:12]))
    if len(content) >= 5:
        candidates.append(" ".join(content[:8]))
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = candidate.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(candidate)
    return deduped


def segment_text(text: str, max_chars: int = 700) -> list[Segment]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n+", normalized) if part.strip()]
    raw_segments: list[str] = []
    for paragraph in paragraphs:
        if looks_like_heading(paragraph):
            continue
        sentences = split_sentences(paragraph)
        if len(sentences) > 1:
            raw_segments.extend(sentences)
        elif len(paragraph) <= max_chars:
            raw_segments.append(re.sub(r"\s+", " ", paragraph))
        else:
            raw_segments.extend(sentences)
    segments: list[Segment] = []
    for idx, segment in enumerate(raw_segments, 1):
        cleaned = clean_text(segment)
        if len(cleaned) < 10:
            continue
        segments.append(
            Segment(
                id=f"S{len(segments) + 1:03d}",
                text=cleaned,
                search_query=query_from_segment(cleaned),
                order=len(segments) + 1,
            )
        )
    return segments


def candidate_from_crossref(item: dict[str, Any], source_query: str) -> Candidate | None:
    journal = first(item.get("container-title"))
    if not journal:
        return None
    family = journal_family(journal) or ""
    start, end = pages(item)
    authors = [author_name(author) for author in item.get("author", [])]
    authors = [author for author in authors if author]
    return Candidate(
        title=clean_text(first(item.get("title"))),
        journal=normalize_title(journal),
        family=family,
        year=year_from_item(item),
        y1=y1_from_item(item),
        doi=item.get("DOI", ""),
        url=item.get("URL", ""),
        volume=item.get("volume", ""),
        issue=item.get("issue", ""),
        start_page=start,
        end_page=end,
        issn=first(item.get("ISSN")),
        authors=authors,
        abstract=clean_text(item.get("abstract", "")),
        type=item.get("type", ""),
        score=float(item.get("score", 0.0) or 0.0),
        source_query=source_query,
    )


def crossref_headers(mailto: str | None = None) -> dict[str, str]:
    return {"User-Agent": USER_AGENT if not mailto else f"codex-nature-citation/1.0 (mailto:{mailto})"}


def fetch_crossref(query: str, rows: int, mailto: str | None = None, from_year: int | None = None, to_year: int | None = None, retries: int = 2) -> list[dict[str, Any]]:
    filters = ["type:journal-article"]
    if from_year is not None:
        filters.append(f"from-pub-date:{from_year}-01-01")
    if to_year is not None:
        filters.append(f"until-pub-date:{to_year}-12-31")
    params = {
        "query.bibliographic": query,
        "rows": str(rows),
        "select": "DOI,title,container-title,published,published-print,published-online,issued,author,volume,issue,page,article-number,ISSN,URL,abstract,type,score",
        "filter": ",".join(filters),
        "sort": "relevance",
        "order": "desc",
    }
    if mailto:
        params["mailto"] = mailto
    url = f"{CROSSREF_API}?{urlencode(params)}"
    req = Request(url, headers=crossref_headers(mailto))
    last_exc: Exception | None = None
    for attempt in range(1, retries + 2):
        try:
            with urlopen(req, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload.get("message", {}).get("items", [])
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt <= retries:
                time.sleep(min(2 ** attempt, 8))
    raise last_exc  # type: ignore[misc]


def fetch_crossref_doi(doi: str, mailto: str | None = None) -> dict[str, Any]:
    url = f"{CROSSREF_API}/{quote(doi.strip(), safe='')}"
    if mailto:
        url = f"{url}?{urlencode({'mailto': mailto})}"
    req = Request(url, headers=crossref_headers(mailto))
    with urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("message", {})


def dedupe(candidates: list[Candidate]) -> list[Candidate]:
    seen: set[str] = set()
    output: list[Candidate] = []
    for candidate in candidates:
        if not candidate.key or candidate.key in seen:
            continue
        seen.add(candidate.key)
        output.append(candidate)
    return output


def build_ris_record(item: Candidate) -> str:
    lines: list[str] = []
    lines.append("TY  - JOUR")
    if item.title:
        lines.append(f"TI  - {ris_escape(item.title)}")
    for author in item.authors:
        lines.append(f"AU  - {ris_escape(author)}")
    if item.journal:
        lines.append(f"T2  - {ris_escape(item.journal)}")
        lines.append(f"JO  - {ris_escape(item.journal)}")
    if item.year:
        lines.append(f"PY  - {ris_escape(item.year)}")
    if item.y1:
        lines.append(f"Y1  - {ris_escape(item.y1)}")
    if item.volume:
        lines.append(f"VL  - {ris_escape(item.volume)}")
    if item.issue:
        lines.append(f"IS  - {ris_escape(item.issue)}")
    if item.start_page:
        lines.append(f"SP  - {ris_escape(item.start_page)}")
    if item.end_page:
        lines.append(f"EP  - {ris_escape(item.end_page)}")
    if item.doi:
        lines.append(f"DO  - {ris_escape(item.doi)}")
    if item.doi_url:
        lines.append(f"UR  - {ris_escape(item.doi_url)}")
    if item.issn:
        lines.append(f"SN  - {ris_escape(item.issn)}")
    lines.append("N1  - Metadata-only candidate. Inspect abstract or publisher page before citing as support.")
    lines.append("ER  -")
    return "\n".join(lines)


def write_ris(candidates: list[Candidate], path: Path) -> None:
    lines: list[str] = []
    for item in candidates:
        lines.append(build_ris_record(item))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_enw_record(item: Candidate) -> str:
    lines: list[str] = []
    lines.append("%0 Journal Article")
    if item.title:
        lines.append(f"%T {ris_escape(item.title)}")
    for author in item.authors:
        lines.append(f"%A {ris_escape(author)}")
    if item.journal:
        lines.append(f"%J {ris_escape(item.journal)}")
    if item.volume:
        lines.append(f"%V {ris_escape(item.volume)}")
    if item.issue:
        lines.append(f"%N {ris_escape(item.issue)}")
    if item.start_page and item.end_page:
        lines.append(f"%P {ris_escape(item.start_page)}-{ris_escape(item.end_page)}")
    elif item.start_page:
        lines.append(f"%P {ris_escape(item.start_page)}")
    if item.year:
        lines.append(f"%D {ris_escape(item.year)}")
    if item.issn:
        lines.append(f"%@ {ris_escape(item.issn)}")
    if item.doi:
        lines.append(f"%R {ris_escape(item.doi)}")
    if item.doi_url:
        lines.append(f"%U {ris_escape(item.doi_url)}")
    return "\n".join(lines)


def write_enw(candidates: list[Candidate], path: Path) -> None:
    lines: list[str] = []
    for item in candidates:
        lines.append(build_enw_record(item))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_zotero_rdf_article(item: Candidate) -> str:
    lines: list[str] = [f'    <bib:Article rdf:about={quoteattr(item.article_resource)}>']
    lines.append("        <z:itemType>journalArticle</z:itemType>")
    if item.journal:
        lines.append(f'        <dcterms:isPartOf rdf:resource={quoteattr(item.journal_resource)}/>')
    if item.authors:
        lines.append("        <bib:authors>")
        lines.append("            <rdf:Seq>")
        for author in item.authors:
            family, given = split_author_parts(author)
            lines.append("                <rdf:li>")
            lines.append("                    <foaf:Person>")
            if family:
                lines.append(f"                        <foaf:surname>{xml_escape(family)}</foaf:surname>")
            if given:
                lines.append(f"                        <foaf:givenName>{xml_escape(given)}</foaf:givenName>")
            lines.append("                    </foaf:Person>")
            lines.append("                </rdf:li>")
        lines.append("            </rdf:Seq>")
        lines.append("        </bib:authors>")
    if item.title:
        lines.append(f"        <dc:title>{xml_escape(item.title)}</dc:title>")
    date_value = zotero_date_value(item)
    if date_value:
        lines.append(f"        <dc:date>{xml_escape(date_value)}</dc:date>")
    lines.append("        <z:libraryCatalog>Crossref</z:libraryCatalog>")
    if item.identifier_url:
        lines.append("        <dc:identifier>")
        lines.append("            <dcterms:URI>")
        lines.append(f"                <rdf:value>{xml_escape(item.identifier_url)}</rdf:value>")
        lines.append("            </dcterms:URI>")
        lines.append("        </dc:identifier>")
    if item.doi:
        lines.append(f"        <dc:identifier>{xml_escape(f'DOI {item.doi}')}</dc:identifier>")
    if item.page_range:
        lines.append(f"        <bib:pages>{xml_escape(item.page_range)}</bib:pages>")
    lines.append(f"        <z:citationKey>{xml_escape(item.zotero_citation_key)}</z:citationKey>")
    lines.append("    </bib:Article>")
    return "\n".join(lines)


def build_zotero_rdf_journal(item: Candidate) -> str:
    lines: list[str] = [f'    <bib:Journal rdf:about={quoteattr(item.journal_resource)}>']
    if item.volume:
        lines.append(f"        <prism:volume>{xml_escape(item.volume)}</prism:volume>")
    if item.journal:
        lines.append(f"        <dc:title>{xml_escape(item.journal)}</dc:title>")
    if item.issue:
        lines.append(f"        <prism:number>{xml_escape(item.issue)}</prism:number>")
    if item.issn:
        lines.append(f"        <dc:identifier>{xml_escape(f'ISSN {item.issn}')}</dc:identifier>")
    lines.append("    </bib:Journal>")
    return "\n".join(lines)


def build_zotero_rdf_document(candidates: list[Candidate]) -> str:
    root_open = [
        "<rdf:RDF",
        *(f' xmlns:{prefix}="{uri}"' for prefix, uri in ZOTERO_RDF_NS.items()),
        ">",
    ]
    journal_map: dict[str, str] = {}
    article_blocks: list[str] = []
    for item in candidates:
        article_blocks.append(build_zotero_rdf_article(item))
        if item.journal and item.journal_resource not in journal_map:
            journal_map[item.journal_resource] = build_zotero_rdf_journal(item)
    sections = ["".join(root_open), *article_blocks, *journal_map.values(), "</rdf:RDF>"]
    return "\n".join(section for section in sections if section)


def write_zotero_rdf(candidates: list[Candidate], path: Path) -> None:
    path.write_text(build_zotero_rdf_document(candidates), encoding="utf-8")


def read_text_inputs(args: argparse.Namespace) -> str:
    parts: list[str] = []
    if args.text:
        parts.extend(args.text)
    if args.text_file:
        parts.append(Path(args.text_file).read_text(encoding="utf-8"))
    return "\n\n".join(part for part in parts if part.strip())


def read_claims(args: argparse.Namespace) -> list[str]:
    claims: list[str] = []
    if args.claim:
        claims.extend(args.claim)
    if args.claim_file:
        for line in Path(args.claim_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                claims.append(line)
    return claims


def read_dois(args: argparse.Namespace) -> list[str]:
    dois: list[str] = []
    if args.doi:
        dois.extend(args.doi)
    if args.doi_file:
        for line in Path(args.doi_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                dois.append(line)
    cleaned = []
    for doi in dois:
        doi = doi.strip()
        doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
        if doi:
            cleaned.append(doi)
    return cleaned


def build_segments(args: argparse.Namespace) -> list[Segment]:
    text = read_text_inputs(args)
    segments = segment_text(text, max_chars=args.segment_chars) if text else []
    claims = read_claims(args)
    for claim in claims:
        cleaned = clean_text(claim)
        if cleaned:
            segments.append(
                Segment(
                    id=f"S{len(segments) + 1:03d}",
                    text=cleaned,
                    search_query=query_from_segment(cleaned),
                    order=len(segments) + 1,
                )
            )
    return segments


def search_segment(segment: Segment, args: argparse.Namespace) -> tuple[list[Candidate], list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    candidates: list[Candidate] = []
    queries = [segment.search_query, *fallback_queries_from_segment(segment.text)]
    seen_queries: set[str] = set()
    for query in queries:
        normalized_query = query.strip().lower()
        if not normalized_query or normalized_query in seen_queries:
            continue
        seen_queries.add(normalized_query)
        try:
            items = retry_with_backoff(
                lambda: fetch_crossref(
                    query,
                    rows=args.rows,
                    mailto=args.mailto,
                    from_year=args.from_year,
                    to_year=args.to_year,
                ),
                max_retries=args.max_retries,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append({"segment_id": segment.id, "query": query, "error": str(exc)})
            continue
        for item in items:
            candidate = candidate_from_crossref(item, source_query=query)
            if candidate and in_scope(candidate.journal, args.scope):
                candidates.append(candidate)
        if dedupe(candidates):
            break
    return dedupe(candidates)[: args.per_segment], errors


def build_mapping(segments: list[Segment], args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[Candidate], list[dict[str, str]]]:
    mapping: list[dict[str, Any]] = []
    all_candidates: list[Candidate] = []
    errors: list[dict[str, str]] = []
    for segment in segments:
        candidates, segment_errors = search_segment(segment, args)
        errors.extend(segment_errors)
        all_candidates.extend(candidates)
        mapping.append(
            {
                "segment": segment,
                "references": candidates,
            }
        )
        if args.sleep:
            time.sleep(args.sleep)
    return mapping, dedupe(all_candidates), errors


def summarize_mapping(mapping: list[dict[str, Any]], references: list[Candidate], errors: list[dict[str, str]]) -> str:
    return (
        f"segments={len(mapping)} "
        f"candidates={len(references)} "
        f"errors={len(errors)}"
    )


def write_export_checkpoint(
    outdir: Path,
    base_path: Path,
    export_format: str,
    references: list[Candidate],
) -> Path:
    del export_format
    partial_output = base_path.with_name(f"{base_path.stem}.partial.candidates.json")
    partial_output.write_text(
        json.dumps(
            {
                "status": "metadata-only candidates; not approved for citation",
                "candidates": [candidate.as_dict() for candidate in references],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return partial_output


def write_final_artifacts(
    mapping: list[dict[str, Any]],
    references: list[Candidate],
    outdir: Path,
    output_path: Path,
    args: argparse.Namespace,
    errors: list[dict[str, str]],
    skipped_segments: int = 0,
) -> tuple[Path, Path, Path]:
    artifact_base = outdir / (output_path.stem if output_path.stem else "citation")
    json_payload = mapping_to_json(mapping, references, args, errors)
    if skipped_segments:
        json_payload["notes"].append(f"Skipped {skipped_segments} segment(s) because --max-segments was set.")
    json_path = artifact_base.with_suffix(".json")
    tsv_path = artifact_base.with_suffix(".tsv")
    report_path = artifact_base.with_suffix(".md")
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_mapping_tsv(mapping, tsv_path)
    write_report(mapping, report_path, args.scope, len(references), args.format, output_path.name)
    return json_path, tsv_path, report_path


def process_segment_batches(
    segments: list[Segment],
    args: argparse.Namespace,
    outdir: Path,
    base_path: Path,
) -> tuple[list[dict[str, Any]], list[Candidate], list[dict[str, str]]]:
    batch_size = resolve_batch_size(len(segments), args)
    batches = chunk_segments(segments, batch_size)
    mapping: list[dict[str, Any]] = []
    references: list[Candidate] = []
    errors: list[dict[str, str]] = []
    if not batches:
        return mapping, references, errors

    for batch_index, batch in enumerate(batches, 1):
        print(
            f"Processing batch {batch_index}/{len(batches)}: segments {batch[0].order}-{batch[-1].order} ({len(batch)} segments)..."
        )
        batch_mapping, batch_references, batch_errors = build_mapping(batch, args)
        mapping.extend(batch_mapping)
        references = dedupe([*references, *batch_references])
        errors.extend(batch_errors)
        partial_output = write_export_checkpoint(outdir, base_path, args.format, references)
        print(
            f"  Batch {batch_index} done: {sum(len(entry['references']) for entry in batch_mapping)} candidates, "
            f"cumulative {len(references)} unique refs."
        )
        print(f"  Checkpoint saved: {partial_output}")
    return mapping, references, errors


def fetch_doi_candidates(dois: list[str], args: argparse.Namespace) -> tuple[list[Candidate], list[dict[str, str]]]:
    candidates: list[Candidate] = []
    errors: list[dict[str, str]] = []
    for doi in dois:
        try:
            item = retry_with_backoff(
                lambda: fetch_crossref_doi(doi, mailto=args.mailto),
                max_retries=args.max_retries,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append({"doi": doi, "error": str(exc)})
            continue
        candidate = candidate_from_crossref(item, source_query=f"doi:{doi}")
        if candidate:
            candidates.append(candidate)
        if args.sleep:
            time.sleep(args.sleep)
    return dedupe(candidates), errors


def mapping_to_json(mapping: list[dict[str, Any]], references: list[Candidate], args: argparse.Namespace, errors: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "status": "metadata-only candidates; not approved for citation",
        "scope": args.scope,
        "from_year": args.from_year,
        "to_year": args.to_year,
        "segment_count": len(mapping),
        "candidate_count": len(references),
        "segments": [
            {
                **entry["segment"].as_dict(),
                "candidates": [candidate.as_dict() for candidate in entry["references"]],
            }
            for entry in mapping
        ],
        "candidates": [candidate.as_dict() for candidate in references],
        "errors": errors,
        "notes": [
            "Crossref metadata can discover candidates but cannot establish semantic support.",
            "No insertion marker or ENW/RIS/RDF record is generated until a screened selection passes validation.",
        ],
    }


def write_mapping_tsv(mapping: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "segment_id",
        "segment_order",
        "segment_text",
        "search_query",
        "support_grade",
        "title",
        "journal",
        "family",
        "year",
        "doi",
        "doi_url",
        "authors",
        "score",
        "screening_note",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for entry in mapping:
            segment: Segment = entry["segment"]
            if not entry["references"]:
                writer.writerow(
                    {
                        "segment_id": segment.id,
                        "segment_order": segment.order,
                        "segment_text": segment.text,
                        "search_query": segment.search_query,
                        "support_grade": "no candidate",
                        "screening_note": "No in-scope candidate found in Crossref metadata search.",
                    }
                )
            for candidate in entry["references"]:
                writer.writerow(
                    {
                        "segment_id": segment.id,
                        "segment_order": segment.order,
                        "segment_text": segment.text,
                        "search_query": segment.search_query,
                        "support_grade": "metadata-only candidate",
                        "title": candidate.title,
                        "journal": candidate.journal,
                        "family": candidate.family,
                        "year": candidate.year,
                        "doi": candidate.doi,
                        "doi_url": candidate.doi_url,
                        "authors": "; ".join(candidate.authors[:10]),
                        "score": candidate.score,
                        "screening_note": "Inspect abstract/publisher page before citing this paper as support.",
                    }
                )


def write_report(
    mapping: list[dict[str, Any]],
    path: Path,
    scope: str,
    reference_count: int,
    export_format: str,
    output_name: str,
) -> None:
    lines = [
        "# Nature Citation Report",
        "",
        "## Search Scope",
        "",
        f"- Scope: `{scope}`",
        f"- Segments: {len(mapping)}",
        f"- Unique metadata candidates: {reference_count}",
        "- Source: Crossref metadata search",
        "- Status: no candidate is approved for citation until semantic screening is recorded.",
        "",
        "## Segment-to-Reference Map",
        "",
    ]
    for entry in mapping:
        segment: Segment = entry["segment"]
        lines.extend([f"### {segment.id}", "", segment.text, ""])
        if not entry["references"]:
            lines.extend(["- No in-scope candidate found.", ""])
            continue
        for candidate in entry["references"]:
            lines.extend(
                [
                    f"- {candidate.title}. *{candidate.journal}* ({candidate.year}). {candidate.doi_url}",
                    f"  - Family: {candidate.family or 'Unclassified'}",
                    "  - Support grade: metadata-only candidate",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "## Next gate",
            "",
            f"- Candidate file: `{output_name}`",
            "- Check abstract or full text and record an evidence locator, checked URL/time, and contradiction/retraction status.",
            "- Only a validated `--screened-selection` may produce ENW, RIS, or Zotero RDF.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_html(
    _mapping: list[dict[str, Any]],
    _references: list[Candidate],
    _outdir: Path,
    _path: Path,
    _export_path: Path,
    _export_format: str,
) -> None:
    """Reject the unsafe legacy metadata-only candidate browser."""

    raise RuntimeError(
        "Candidate-browser export is disabled: metadata-only candidates must "
        "be semantically screened before reference-manager export."
    )

def load_screened_selection(
    path: Path,
    candidates: list[Candidate],
    segments: list[Segment],
) -> tuple[list[Candidate], list[dict[str, Any]]]:
    """Validate a human/agent-reviewed claim-to-source selection.

    Discovery metadata is deliberately insufficient. Every exported item must
    identify the manuscript segment, semantic evidence level and locator,
    checked source, check time, and contradiction/retraction screening result.
    """

    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("selections") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ValueError("screened selection must be a list or an object with 'selections'")

    candidate_by_id: dict[str, Candidate] = {}
    for candidate in candidates:
        candidate_by_id[candidate.key] = candidate
        if candidate.doi:
            candidate_by_id[candidate.doi.lower()] = candidate
    segment_ids = {segment.id for segment in segments}

    selected: list[Candidate] = []
    audit: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, raw in enumerate(records, 1):
        if not isinstance(raw, dict):
            errors.append(f"selection {index}: expected an object")
            continue
        segment_id = str(raw.get("segment_id", "")).strip()
        identity = str(raw.get("doi") or raw.get("candidate_key") or "").strip().lower()
        support_grade = str(raw.get("support_grade", "")).strip().lower()
        evidence_basis = str(raw.get("evidence_basis", "")).strip().lower()
        evidence_locator = str(raw.get("evidence_locator", "")).strip()
        checked_url = str(raw.get("checked_url", "")).strip()
        checked_at = str(raw.get("checked_at", "")).strip()
        contradiction_status = str(raw.get("contradiction_status", "")).strip().lower()
        retraction_status = str(raw.get("retraction_status", "")).strip().lower()
        evidence_note = str(
            raw.get("evidence_excerpt") or raw.get("evidence_paraphrase") or ""
        ).strip()

        if segment_id not in segment_ids:
            errors.append(f"selection {index}: unknown segment_id {segment_id!r}")
        candidate = candidate_by_id.get(identity)
        if not identity or candidate is None:
            errors.append(f"selection {index}: DOI/candidate_key not found in this run")
        if support_grade not in SCREENED_SUPPORT_GRADES:
            errors.append(
                f"selection {index}: support_grade must be one of "
                f"{sorted(SCREENED_SUPPORT_GRADES)}"
            )
        if evidence_basis not in SCREENED_EVIDENCE_LEVELS:
            errors.append(
                f"selection {index}: evidence_basis must be one of "
                f"{sorted(SCREENED_EVIDENCE_LEVELS)}"
            )
        if not evidence_locator:
            errors.append(f"selection {index}: evidence_locator is required")
        if not evidence_note:
            errors.append(
                f"selection {index}: evidence_excerpt or evidence_paraphrase is required"
            )
        if not re.match(r"^https?://", checked_url):
            errors.append(f"selection {index}: checked_url must be an HTTP(S) URL")
        if not checked_at:
            errors.append(f"selection {index}: checked_at is required")
        if contradiction_status != "none_found":
            errors.append(
                f"selection {index}: contradiction_status must be 'none_found' for export"
            )
        if retraction_status != "none_found":
            errors.append(
                f"selection {index}: retraction_status must be 'none_found' for export"
            )
        if candidate is not None:
            selected.append(candidate)
            audit.append(
                {
                    **raw,
                    "segment_id": segment_id,
                    "doi": candidate.doi,
                    "candidate_key": candidate.key,
                    "citation_marker": candidate.citation_marker,
                }
            )

    if errors:
        raise ValueError("invalid screened selection:\n- " + "\n- ".join(errors))
    return dedupe(selected), audit


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Discover Nature/CNS citation candidates; export references only "
            "from a semantically screened selection."
        )
    )
    parser.add_argument("--text", action="append", help="Manuscript text to segment and cite. Can be repeated.")
    parser.add_argument("--text-file", help="UTF-8 manuscript text file.")
    parser.add_argument("--claim", action="append", help="Single claim to treat as one segment. Can be repeated.")
    parser.add_argument("--claim-file", help="UTF-8 text file with one claim per line.")
    parser.add_argument("--doi", action="append", help="Known DOI to fetch and export. Can be repeated.")
    parser.add_argument("--doi-file", help="UTF-8 text file with one DOI per line.")
    parser.add_argument(
        "--screened-selection",
        help=(
            "JSON selection with support grade, evidence basis/locator, checked "
            "URL/time, and contradiction/retraction screening."
        ),
    )
    parser.add_argument("--scope", choices=["cns", "nature", "science", "cell", "flagship"], default="cns")
    parser.add_argument("--output-file", help="Reference output file path, typically ending in .enw, .ris, or .rdf.")
    parser.add_argument("--outdir", help="Optional directory for outputs. If omitted, uses the output file parent or current directory.")
    parser.add_argument("--format", choices=EXPORT_FORMAT_CHOICES, help="Reference export format: enw, ris, or zotero-rdf. Inferred from --output-file when omitted.")
    parser.add_argument(
        "--with-artifacts",
        action="store_true",
        help="Also generate JSON/TSV/Markdown candidate-review artifacts.",
    )
    parser.add_argument("--rows", type=int, default=30, help="Crossref rows per segment before journal-scope filtering.")
    parser.add_argument("--per-segment", type=int, default=3, help="Maximum candidates to keep per segment.")
    parser.add_argument("--segment-chars", type=int, default=700, help="Split paragraphs longer than this many characters.")
    parser.add_argument("--max-candidates", type=int, default=80, help="Maximum deduplicated references to export.")
    parser.add_argument("--max-segments", type=int, help="Limit the number of segments processed in a single run.")
    parser.add_argument("--batch-size", type=int, help="Process segments in batches of this size.")
    parser.add_argument("--max-retries", type=int, default=2, help="Maximum retry count for Crossref requests.")
    parser.add_argument("--from-year", type=int, help="Earliest publication year.")
    parser.add_argument("--to-year", type=int, help="Latest publication year.")
    parser.add_argument("--mailto", help="Email for Crossref polite pool.")
    parser.add_argument("--sleep", type=float, default=0.3, help="Seconds between Crossref requests.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    segments = build_segments(args)
    dois = read_dois(args)
    if not segments and not dois:
        print("Provide --text, --text-file, --claim, --claim-file, --doi, or --doi-file.", file=sys.stderr)
        return 2

    screened_selection = (
        Path(args.screened_selection).expanduser().resolve()
        if args.screened_selection
        else None
    )
    output_path = Path(args.output_file).expanduser().resolve() if args.output_file else None
    if args.outdir:
        outdir = Path(args.outdir).expanduser().resolve()
    elif output_path:
        outdir = output_path.parent
    else:
        outdir = Path.cwd().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    args.format = normalize_export_format(args.format) if args.format else infer_export_format(output_path)

    # Derive a meaningful base name from input text when no explicit output file was given
    raw_text = read_text_inputs(args)
    name_base = slug_from_text(raw_text) if not args.output_file else None

    if output_path is None:
        output_path = (
            outdir / export_filename(args.format, base="references")
            if screened_selection
            else outdir / f"{name_base or 'citation'}-candidates.json"
        )
    if screened_selection is None and output_path.suffix.lower() != ".json":
        print(
            "Candidate discovery can only write JSON. Use --screened-selection "
            "before requesting ENW/RIS/RDF export.",
            file=sys.stderr,
        )
        return 2

    segments, skipped_segments = limit_segments(segments, args.max_segments or 0)
    mapping, references, errors = process_segment_batches(segments, args, outdir, output_path)
    doi_candidates, doi_errors = fetch_doi_candidates(dois, args)
    errors.extend(doi_errors)
    references = dedupe([*references, *doi_candidates])[: args.max_candidates]

    if screened_selection is None:
        candidate_payload = mapping_to_json(mapping, references, args, errors)
        if skipped_segments:
            candidate_payload["notes"].append(
                f"Skipped {skipped_segments} segment(s) because --max-segments was set."
            )
        output_path.write_text(
            json.dumps(candidate_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if args.with_artifacts:
            json_path, tsv_path, report_path = write_final_artifacts(
                mapping,
                references,
                outdir,
                output_path,
                args,
                errors,
                skipped_segments=skipped_segments,
            )
            print(f"Candidate review artifacts: {tsv_path}, {json_path}, {report_path}")
        print(f"Candidate output: {output_path}")
        print(f"Unique metadata candidates: {len(references)}")
        print(
            "No citation markers or reference-manager files were generated; "
            "screen semantic support first."
        )
        return 0

    try:
        selected_references, screening_audit = load_screened_selection(
            screened_selection,
            references,
            segments,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2

    # Final export is possible only after the separate semantic-screening gate.
    if args.format == "enw":
        write_enw(selected_references, output_path)
    elif args.format == "ris":
        write_ris(selected_references, output_path)
    else:
        write_zotero_rdf(selected_references, output_path)
    audit_path = output_path.with_name(f"{output_path.stem}.screening.json")
    audit_path.write_text(
        json.dumps(
            {
                "screened_selection": str(screened_selection),
                "export_format": args.format,
                "exported_count": len(selected_references),
                "selections": screening_audit,
                "retrieval_errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Reference output: {output_path}")
    print(f"Screening audit: {audit_path}")
    print(f"Export format: {args.format} ({export_label(args.format)})")
    print(f"Screened references exported: {len(selected_references)}")
    if skipped_segments:
        print(f"Segments skipped: {skipped_segments}")
    if errors:
        print(
            f"Encountered {len(errors)} retrieval error(s); see the screening audit.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
