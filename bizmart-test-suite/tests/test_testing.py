"""Aspek Testing -- NFR-029 s.d. NFR-032."""
import subprocess, re
from conftest import SUT_DIR, login


def test_NFR029_sut_has_automated_tests():
    found = [p for p in SUT_DIR.rglob("*") if ".git" not in p.parts and re.search(r"(test|spec)", p.name, re.I)
             and p.is_file()]
    assert found, "Tidak ada berkas test di repositori SUT"


def test_NFR030_logic_testable_without_dom(js, tmp_path):
    f = tmp_path / "app.js"
    f.write_text(js, encoding="utf-8")
    r = subprocess.run(["node", "-e", f"require('vm').runInNewContext(require('fs').readFileSync('{f}','utf8'),{{}})"],
                       capture_output=True, text=True)
    assert r.returncode == 0, "Logika tidak dapat dimuat tanpa DOM/localStorage"


def test_NFR031_negative_boundary_product_rejected(admin):
    admin.evaluate("openProductModal()")
    admin.fill("#pm-name", "Produk Negatif")
    admin.select_option("#pm-category", index=1)
    admin.fill("#pm-price", "-5000")
    admin.fill("#pm-stock", "-10")
    admin.evaluate("saveProduct()")
    bad = admin.evaluate("products.some(p => p.name === 'Produk Negatif' && (p.price < 0 || p.stock < 0))")
    assert not bad, "Produk dengan harga/stok negatif diterima"


def test_NFR032_e2e_flow_automatable(page):
    login(page, "user@bizmart.id", "user123")
    assert page.is_visible("#app")
    page.evaluate("addToCart(3)")
    page.evaluate("checkout()")
    page.fill("#shipping-address", "Jl. E2E No.1")
    page.evaluate("confirmCheckout()")
    page.evaluate("doLogout()")
    assert page.is_visible("#auth-screen")
