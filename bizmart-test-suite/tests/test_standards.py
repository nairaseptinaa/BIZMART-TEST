"""Aspek Adherence to Standards -- NFR-025 s.d. NFR-028."""
import re


def test_NFR025_prefer_const(eslint_counts):
    assert eslint_counts.get("prefer-const", 0) == 0


def test_NFR025_strict_equality(eslint_counts):
    assert eslint_counts.get("eqeqeq", 0) == 0


def test_NFR026_html_valid_htmlhint(htmlhint_errors):
    assert htmlhint_errors == 0


def test_NFR027_labels_have_for_attribute(html):
    labels = re.findall(r"<label\b[^>]*>", html)
    missing = [l for l in labels if "for=" not in l]
    assert not missing, f"{len(missing)} dari {len(labels)} label tanpa atribut for"


def test_NFR027_aria_attributes_present(html):
    assert html.count("aria-") > 0, "Tidak ada atribut aria-*"


def test_NFR028_no_blocking_dialog(eslint_counts):
    assert eslint_counts.get("no-alert", 0) == 0
