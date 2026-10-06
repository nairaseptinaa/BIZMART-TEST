"""Aspek Maintainability -- NFR-005 s.d. NFR-008."""
import re, pathlib
from conftest import SUT_DIR


def test_NFR005_js_separated_into_modules():
    js_files = [p for p in SUT_DIR.rglob("*.js") if ".git" not in p.parts]
    assert len(js_files) >= 2, f"Hanya {len(js_files)} berkas JS; seluruh logika di satu file HTML"


def test_NFR006_no_duplicate_date_formatting(js):
    n = len(re.findall(r"toLocaleDateString\('id-ID'", js))
    assert n <= 1, f"Format tanggal diduplikasi {n}x"


def test_NFR006_no_duplicate_initials_logic(js):
    n = len(re.findall(r"split\(' '\)\.map\(w=>w\[0\]\)", js))
    assert n <= 1, f"Pembuatan inisial nama diduplikasi {n}x"


def test_NFR007_data_separated_from_logic(js):
    mutable_globals = re.findall(r"^let \w+", js, re.M)
    assert len(mutable_globals) == 0, f"{len(mutable_globals)} state global 'let' bercampur dengan logika"


def test_NFR008_status_list_single_source(js):
    n = len(re.findall(r"\[\s*'pending'\s*,\s*'processing'", js))
    assert n <= 1, f"Daftar status pesanan didefinisikan di {n} tempat"
