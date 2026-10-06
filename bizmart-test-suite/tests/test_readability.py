"""Aspek Readability -- NFR-009 s.d. NFR-012."""
import re


def test_NFR009_names_are_camelCase_and_descriptive(js):
    names = re.findall(r"^function (\w+)\(", js, re.M)
    assert names
    bad = [n for n in names if not re.fullmatch(r"[a-z]+([A-Z][a-z0-9]*)*", n) or len(n) < 4]
    assert not bad, f"Nama fungsi tidak konsisten: {bad}"


def test_NFR010_indentation_consistent(js):
    assert not re.search(r"^\t", js, re.M), "Tab dan spasi bercampur"
    assert re.findall(r"// =+ \w", js), "Tidak ada penanda seksi"


def test_NFR011_no_scattered_magic_strings(js):
    n = len(re.findall(r"(===|!==)\s*'(pending|processing|shipped|delivered|cancelled)'", js))
    assert n == 0, f"{n} perbandingan status memakai string literal langsung"


def test_NFR012_functions_max_40_lines(eslint_counts):
    assert eslint_counts.get("max-lines-per-function", 0) == 0, \
        f"{eslint_counts.get('max-lines-per-function')} fungsi melebihi 40 baris"
