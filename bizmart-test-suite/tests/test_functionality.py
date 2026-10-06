"""Aspek Functionality -- NFR-017 s.d. NFR-020."""
from conftest import SUT_URL, login


def test_NFR017_corrupt_storage_handled(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.add_init_script("localStorage.setItem('bm_orders', '{rusak')")
    pg.goto(SUT_URL)
    ctx.close()
    assert not errors, f"Skrip berhenti saat load: {errors[0][:80]}"


def test_NFR018_cart_total_correct(user):
    user.evaluate("addToCart(1); addToCart(1); addToCart(5)")
    assert "111.000" in user.inner_text("#cart-total-value")


def test_NFR018_checkout_creates_order_and_clears_cart(user):
    user.evaluate("addToCart(1); addToCart(5)")
    user.evaluate("checkout()")
    user.fill("#shipping-address", "Jl. Uji No.1, Malang")
    user.evaluate("confirmCheckout()")
    assert user.evaluate("cart.length") == 0
    assert user.evaluate("orders[orders.length-1].total") == 93000


def test_NFR019_stock_never_negative(user):
    user.evaluate("products.find(p => p.id === 2).stock = 2")
    user.evaluate("addToCart(2); updateCartQty(2, 3)")      # qty 4 > stok 2
    user.evaluate("checkout()")
    user.fill("#shipping-address", "Jl. Uji No.1")
    user.evaluate("confirmCheckout()")
    stock = user.evaluate("products.find(p => p.id === 2).stock")
    assert stock >= 0, f"Stok akhir {stock}"


def test_NFR020_user_cancel_restores_stock(user):
    before = user.evaluate("products.find(p => p.id === 2).stock")
    user.evaluate("cancelOrder('BM-003')")
    assert user.evaluate("products.find(p => p.id === 2).stock") == before + 1


def test_NFR020_admin_cancel_restores_stock(admin):
    before = admin.evaluate("products.find(p => p.id === 2).stock")
    admin.evaluate("updateOrderStatus('BM-003', 'cancelled')")
    assert admin.evaluate("products.find(p => p.id === 2).stock") == before + 1, \
        "Stok tidak kembali saat admin membatalkan"
