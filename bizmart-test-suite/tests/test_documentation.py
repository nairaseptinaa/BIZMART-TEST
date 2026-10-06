"""Aspek Documentation & Comment -- NFR-021 s.d. NFR-024."""
import re
from conftest import SUT_DIR


def test_NFR021_functions_have_doc_comments(js):
    lines = js.splitlines()
    idx = [i for i, l in enumerate(lines) if re.match(r"function \w+\(", l)]
    documented = sum(1 for i in idx if i > 0 and re.match(r"\s*(/\*\*|\*/|//(?! =))", lines[i - 1]))
    ratio = documented / len(idx)
    assert ratio >= 0.8, f"Hanya {documented}/{len(idx)} fungsi berkomentar ({ratio:.0%})"


def test_NFR022_readme_exists(readme):
    assert len(readme) > 500


def test_NFR023_readme_matches_code(readme):
    names = set(re.findall(r"[\w-]+\.html", readme))
    existing = {p.name for p in SUT_DIR.glob("*.html")}
    assert names <= existing, f"README menyebut {names - existing} yang tidak ada"


def test_NFR024_readme_has_run_instructions(readme):
    assert "Cara Menjalankan" in readme


def test_NFR024_readme_lists_demo_accounts(readme):
    assert "admin@bizmart.id" in readme and "user@bizmart.id" in readme
