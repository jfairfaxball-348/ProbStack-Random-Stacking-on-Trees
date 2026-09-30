#!/usr/bin/env python3
"""Build and validate the self-contained ProbStack arXiv source archive."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

PAPER = Path(__file__).resolve().parent
ARXIV = PAPER / "arxiv"
BUILD = PAPER / ".build" / "arxiv"
CANONICAL = PAPER / "main.tex"
PACKAGED = ARXIV / "main.tex"
METADATA = ARXIV / "metadata.txt"
TARGET = ARXIV / "ProbStack-arxiv.tar.gz"
CHECKSUM = ARXIV / "archive.sha256"
PALOMAR_ID = "PALOMAR-2026-09-30-000023"
PALOMAR_URL = "https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-30-000023&version=1"
EXPECTED_TITLE = "A Fixed-Offset Transition for Random Stackability on Paths"
EXPECTED_AUTHOR = "John Fairfax-Ball"
EXPECTED_PAGES = 16
EXPECTED_FIGURES = 0
EXPECTED_REFS = 14
EXPECTED_SOURCE_COMMIT = "f37d04ee93168b1f3ab1ff271fc850e8dad2955c"
FIELDS = (
    "Title", "Authors", "Abstract", "Comments", "Primary category", "Cross-list",
    "MSC-class", "Intended license", "Report-no", "Journal-ref", "DOI",
    "Palomar verification", "Palomar scope", "Repository", "Standalone source commit",
)


class PreflightError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PreflightError(message)


def tool(name: str) -> str:
    path = shutil.which(name)
    require(path is not None, f"Required command not found on PATH: {name}")
    return path


def command(args: list[str], cwd: Path) -> str:
    env = os.environ.copy()
    env["LC_ALL"] = "C"
    for key in ("TEXINPUTS", "BIBINPUTS", "BSTINPUTS"):
        env.pop(key, None)
    result = subprocess.run(
        args, cwd=cwd, env=env, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    require(
        result.returncode == 0,
        f"Command failed in {cwd}: {' '.join(args)}\n{result.stdout[-16000:]}",
    )
    return result.stdout


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def without_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def metadata() -> dict[str, str]:
    raw = METADATA.read_text(encoding="utf-8")
    require(raw.isascii(), "arXiv metadata must be ASCII")
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        key, sep, value = line.partition(":")
        if sep and key in FIELDS:
            require(key not in fields, f"Duplicate metadata field: {key}")
            fields[key] = value.strip()
    require(set(fields) == set(FIELDS), f"Missing metadata fields: {set(FIELDS) - set(fields)}")
    require(fields["Title"] == EXPECTED_TITLE, "Metadata title mismatch")
    require(fields["Authors"] == EXPECTED_AUTHOR, "Metadata author mismatch")
    require(0 < len(fields["Abstract"]) <= 1920, "Metadata abstract must be 1..1920 characters")
    require("\\eps" not in fields["Abstract"], "Expand local \\eps macro in metadata abstract")
    require("\\emph" not in fields["Abstract"], "Remove font commands from metadata abstract")
    require(fields["Primary category"] == "math.CO", "Unexpected primary category")
    require(fields["Cross-list"] == "None", "Unexpected cross-list")
    require(fields["MSC-class"] == "05C99", "Unexpected MSC classification")
    require(fields["Intended license"].startswith("CC BY 4.0"), "Unexpected intended license")
    require(fields["Report-no"] == "", "Report-no must remain empty unless established")
    require(fields["Journal-ref"] == "", "Journal-ref must remain empty unless established")
    require(fields["DOI"] == "", "DOI must remain empty unless established")
    require(fields["Palomar verification"] == PALOMAR_URL, "Palomar URL mismatch")
    require(
        "does not register the full probabilistic fixed-offset transition theorem"
        in fields["Palomar scope"],
        "Palomar scope must explicitly exclude the probabilistic theorem",
    )
    require(fields["Standalone source commit"] == EXPECTED_SOURCE_COMMIT, "Standalone source commit mismatch")
    return fields


def source_checks(text: str) -> None:
    clean = without_comments(text)
    require(
        CANONICAL.read_bytes() == PACKAGED.read_bytes(),
        "paper/arxiv/main.tex must be byte-for-byte identical to paper/main.tex",
    )
    require(
        r"\title{A Fixed-Offset Transition for Random Stackability on Paths}" in clean,
        "Title changed",
    )
    require(r"\author{John Fairfax-Ball}" in clean, "Author changed")
    require(
        r"c_n=\sqrt{\log_2 n}-\frac12\log_2\log_2 n+\log_2(3e)" in clean,
        "Main theorem centre changed",
    )
    require(
        r"No assertion is made when the offset tends to $0$." in clean,
        "Zero-offset boundary missing",
    )
    require(r"$\EMPTY$ is not the integer $0$" in clean, "Categorical EMPTY boundary missing")
    require(r"m\le-(2\mu-1)" in clean, "Exact fixed-total deep-message target changed")
    require(PALOMAR_ID in clean, "Palomar identifier missing from manuscript")
    require(
        "It does \\emph{not} cover the full" in clean and "probabilistic Theorem" in clean,
        "Palomar scope wording no longer excludes the probabilistic theorem",
    )
    require(clean.count(r"\bibitem{") == EXPECTED_REFS, "Unexpected bibliography reference count")
    require(
        clean.count(r"\begin{figure}") + clean.count(r"\begin{figure*}") == EXPECTED_FIGURES,
        "Unexpected figure count",
    )
    require(
        not re.search(r"\\(?:input|include|includegraphics|bibliography)\s*\{", clean),
        "Package is no longer a single self-contained TeX input",
    )
    require(
        not re.search(r"\b(?:TODO|FIXME|TBD)\b|PLACEHOLDER|\?\?", clean),
        "Unresolved editorial marker in manuscript",
    )


def compile_tex(source: Path, directory: Path, pdflatex: str) -> str:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)
    shutil.copyfile(source, directory / "main.tex")
    args = [
        pdflatex,
        "-no-shell-escape",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "main.tex",
    ]
    log = ""
    for _ in range(4):
        command(args, directory)
        log = (directory / "main.log").read_text(encoding="utf-8", errors="replace")
        if not re.search(r"Rerun to get|Label\(s\) may have changed|rerunfilecheck Warning", log):
            break
    return log


def check_log(log: str, label: str) -> None:
    bad = []
    for line in log.splitlines():
        if re.search(
            r"^!|LaTeX Error|undefined references|undefined citations|multiply defined|"
            r"Overfull \\[hv]box|Rerun to get|Label\(s\) may have changed|"
            r"rerunfilecheck Warning|Missing character:",
            line,
            flags=re.IGNORECASE,
        ):
            bad.append(line)
    require(not bad, f"{label} failed:\n" + "\n".join(bad))


def pdf_details(directory: Path, pdfinfo: str, pdftotext: str) -> tuple[int, str]:
    info = command([pdfinfo, "main.pdf"], directory)
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    require(match is not None, "Cannot determine PDF page count")
    command([pdftotext, "-layout", "main.pdf", "main.txt"], directory)
    text = (directory / "main.txt").read_text(encoding="utf-8", errors="replace")
    require("\ufffd" not in text, "Replacement character in extracted PDF text")
    require(len(text.strip()) > 1000, "Extracted PDF text unexpectedly short")
    return int(match.group(1)), text


def make_archive(source: Path, target: Path) -> None:
    data = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as out:
        with gzip.GzipFile(filename="", mode="wb", fileobj=out, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tar:
                item = tarfile.TarInfo("main.tex")
                item.size = len(data)
                item.mode = 0o644
                item.mtime = 0
                item.uid = item.gid = 0
                item.uname = item.gname = ""
                tar.addfile(item, io.BytesIO(data))


def safe_extract(archive_path: Path, directory: Path) -> list[str]:
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)
    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        require(names == ["main.tex"], f"Unexpected archive members: {names}")
        member = tar.getmember("main.tex")
        require(
            member.isfile() and not member.issym() and not member.islnk(),
            "Unsafe archive member",
        )
        stream = tar.extractfile(member)
        require(stream is not None, "Cannot read main.tex from archive")
        (directory / "main.tex").write_bytes(stream.read())
    return names


def main() -> None:
    require(CANONICAL.is_file(), "Missing paper/main.tex")
    require(PACKAGED.is_file(), "Missing paper/arxiv/main.tex")
    require(METADATA.is_file(), "Missing paper/arxiv/metadata.txt")

    source = PACKAGED.read_text(encoding="utf-8")
    source_checks(source)
    fields = metadata()

    pdflatex = tool("pdflatex")
    pdfinfo = tool("pdfinfo")
    pdftotext = tool("pdftotext")
    BUILD.mkdir(parents=True, exist_ok=True)

    canonical_dir = BUILD / "canonical"
    packaged_dir = BUILD / "packaged"
    extracted_dir = BUILD / "extracted"

    log = compile_tex(CANONICAL, canonical_dir, pdflatex)
    check_log(log, "Canonical compilation")
    canonical_pages, canonical_text = pdf_details(canonical_dir, pdfinfo, pdftotext)

    log = compile_tex(PACKAGED, packaged_dir, pdflatex)
    check_log(log, "Packaged-source compilation")
    packaged_pages, packaged_text = pdf_details(packaged_dir, pdfinfo, pdftotext)
    require(
        (canonical_pages, canonical_text) == (packaged_pages, packaged_text),
        "Packaged-source PDF text differs from canonical PDF",
    )

    require(
        canonical_pages == EXPECTED_PAGES,
        f"Expected {EXPECTED_PAGES} pages, got {canonical_pages}",
    )
    text_flat = normalized(canonical_text)
    require(EXPECTED_TITLE in text_flat, "Compiled PDF title mismatch")
    require(EXPECTED_AUTHOR in text_flat, "Compiled PDF author mismatch")
    require(PALOMAR_ID in text_flat, "Palomar identifier missing from compiled PDF")
    require(
        "No assertion is made at zero offset." in text_flat,
        "Zero-offset disclaimer missing from compiled PDF",
    )
    require(
        "16 pages" in fields["Comments"] and "0 figures" in fields["Comments"],
        "Comments field must state actual page/figure counts",
    )

    candidate = BUILD / "ProbStack-arxiv.tar.gz"
    make_archive(PACKAGED, candidate)
    archive_to_test = candidate
    if TARGET.exists():
        require(
            TARGET.read_bytes() == candidate.read_bytes(),
            "Committed arXiv archive is stale or differs from deterministic rebuild",
        )
        archive_to_test = TARGET

    members = safe_extract(archive_to_test, extracted_dir)
    rebuild_dir = extracted_dir / "rebuild"
    log = compile_tex(extracted_dir / "main.tex", rebuild_dir, pdflatex)
    check_log(log, "Extracted-archive compilation")
    rebuilt_pages, rebuilt_text = pdf_details(rebuild_dir, pdfinfo, pdftotext)
    require(
        (canonical_pages, canonical_text) == (rebuilt_pages, rebuilt_text),
        "Extracted archive PDF text/page count differs from canonical build",
    )

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(candidate, TARGET)
    digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    CHECKSUM.write_text(f"{digest}  {TARGET.name}\n", encoding="ascii")

    report = {
        "status": "ARXIV PACKAGE PREFLIGHT PASS",
        "standalone_source_commit": EXPECTED_SOURCE_COMMIT,
        "canonical_sha256": hashlib.sha256(CANONICAL.read_bytes()).hexdigest(),
        "packaged_source_sha256": hashlib.sha256(PACKAGED.read_bytes()).hexdigest(),
        "archive": str(TARGET.relative_to(PAPER.parent)),
        "archive_sha256": digest,
        "archive_members": members,
        "page_count": canonical_pages,
        "figure_count": EXPECTED_FIGURES,
        "reference_count": EXPECTED_REFS,
        "title": EXPECTED_TITLE,
        "author": EXPECTED_AUTHOR,
        "primary_category": fields["Primary category"],
        "cross_list": fields["Cross-list"],
        "intended_license": fields["Intended license"],
        "palomar_id": PALOMAR_ID,
        "palomar_scope": fields["Palomar scope"],
        "pdf_committed": False,
    }
    (BUILD / "preflight.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    shutil.copyfile(rebuild_dir / "main.pdf", BUILD / "ProbStack-arxiv.pdf")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
