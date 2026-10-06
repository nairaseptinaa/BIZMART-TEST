"""Aspek Performance -- NFR-013 s.d. NFR-016."""
import re, time


def test_NFR013_filter_algorithm_scales(user):
    ms = user.evaluate("""() => {
      const base = products[0];
      for (let i = 0; i < 5000; i++) products.push({...base, id: 1000 + i, name: 'Produk ' + i});
      const t = performance.now(); renderProducts(); return performance.now() - t; }""")
    assert ms < 500, f"renderProducts 5000 produk = {ms:.0f} ms"


def test_NFR014_no_unneeded_rerender(user):
    # Membatalkan pesanan produk #2 tidak boleh merender ulang kartu produk lain
    user.evaluate("document.querySelector('.product-card').dataset.mark = 'ya'")
    user.evaluate("cancelOrder('BM-003')")
    still = user.evaluate("document.querySelectorAll('.product-card[data-mark]').length")
    assert still == 1, "Seluruh grid dirender ulang (kartu yang tidak berubah ikut diganti)"


def test_NFR015_savedata_writes_only_changed_key(admin):
    n = admin.evaluate("""() => { let c = 0; const o = Storage.prototype.setItem;
      Storage.prototype.setItem = function(k, v) { c++; return o.call(this, k, v); };
      updateOrderStatus('BM-003', 'shipped'); Storage.prototype.setItem = o; return c; }""")
    assert n <= 1, f"saveData() menulis {n} key localStorage untuk 1 perubahan"


def test_NFR016_no_heavy_dependencies(html):
    assert not re.search(r"<script[^>]+src=", html), "Ada library JS eksternal"
