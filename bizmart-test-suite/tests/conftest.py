import json, os, re, subprocess, pathlib, collections
import pytest
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUT_DIR = pathlib.Path(os.environ.get("SUT_DIR", ROOT / "sut" / "bizmart-umkm"))
SUT_HTML = SUT_DIR / "bizmart-umkm.html"
SUT_URL = SUT_HTML.resolve().as_uri()


@pytest.fixture(scope="session")
def html():
    return SUT_HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def js(html):
    return re.search(r"<script>(.*)</script>", html, re.S).group(1)


@pytest.fixture(scope="session")
def readme():
    return (SUT_DIR / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def eslint_counts(js, tmp_path_factory):
    """Jalankan ESLint (config eslintrc.sut.json) pada JS hasil ekstraksi SUT."""
    d = tmp_path_factory.mktemp("eslint")
    (d / "app.js").write_text(js, encoding="utf-8")
    out = subprocess.run(
        ["npx", "eslint", "--no-eslintrc", "-c", str(ROOT / "eslintrc.sut.json"),
         "-f", "json", str(d / "app.js")],
        cwd=ROOT, capture_output=True, text=True)
    data = json.loads(out.stdout)[0]["messages"]
    return collections.Counter(m["ruleId"] for m in data)


@pytest.fixture(scope="session")
def htmlhint_errors():
    out = subprocess.run(["npx", "htmlhint", "-f", "json", str(SUT_HTML)],
                         cwd=ROOT, capture_output=True, text=True)
    data = json.loads(out.stdout)
    return sum(len(f["messages"]) for f in data)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture()
def page(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    pg.goto(SUT_URL)
    yield pg
    ctx.close()


def login(pg, email, password):
    pg.fill("#login-email", email)
    pg.fill("#login-password", password)
    pg.evaluate("doLogin()")


@pytest.fixture()
def admin(page):
    login(page, "admin@bizmart.id", "admin123")
    return page


@pytest.fixture()
def user(page):
    login(page, "user@bizmart.id", "user123")
    return page
