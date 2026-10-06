"""Aspek Security -- NFR-001 s.d. NFR-004 (kriteria checklist Security no. 1-4)."""
import re
from conftest import login


def test_NFR001_no_hardcoded_credentials(js):
    # Tidak boleh ada literal password di source code
    assert not re.search(r"password\s*:\s*'[^']+'", js), "Password literal ditemukan di DEMO_USERS"


def test_NFR002_password_is_hashed(page):
    page.evaluate("switchAuthTab('register')")
    page.fill("#reg-name", "Penguji")
    page.fill("#reg-email", "penguji@test.id")
    page.fill("#reg-password", "RahasiaKu123")
    page.evaluate("doRegister()")
    stored = page.evaluate("localStorage.getItem('bm_users')")
    assert "RahasiaKu123" not in stored, "Password tersimpan plaintext di localStorage"


def test_NFR003_xss_not_executed_on_admin_page(page):
    page.evaluate("switchAuthTab('register')")
    page.fill("#reg-name", "<img src=x onerror=window.__xss=1>")
    page.fill("#reg-email", "xss@test.id")
    page.fill("#reg-password", "abcdef")
    page.evaluate("doRegister()")
    page.evaluate("doLogout()")
    page.evaluate("switchAuthTab('login')")
    login(page, "admin@bizmart.id", "admin123")
    page.evaluate("showPage('admin-users')")
    page.wait_for_timeout(300)
    assert page.evaluate("window.__xss") is None, "Payload XSS dieksekusi di halaman admin"


def test_NFR003_eslint_no_unsanitized_innerhtml(eslint_counts):
    assert eslint_counts.get("no-unsanitized/property", 0) == 0


def test_NFR004_role_authorization_deleteProduct(user):
    before = user.evaluate("products.length")
    user.evaluate("deleteProduct(1)")
    after = user.evaluate("products.length")
    assert after == before, "User biasa berhasil menghapus produk lewat konsol"


def test_NFR004_review_requires_order_ownership(page):
    login(page, "kurnia@bizmart.id", "kurnia123")   # bukan pemilik BM-001
    before = page.evaluate("reviews.length")
    page.evaluate("openReviewModal('BM-001', 2)")
    page.fill("#review-comment", "Ulasan tanpa kepemilikan")
    page.evaluate("submitReview()")
    assert page.evaluate("reviews.length") == before, "Ulasan diterima tanpa cek kepemilikan pesanan"
