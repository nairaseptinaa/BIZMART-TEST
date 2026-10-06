# Test Suite Bizmart UMKM (Kelompok 3)

Prasyarat: Node.js 22, Python 3.12, `pip install pytest playwright && playwright install chromium`,
`npm i --legacy-peer-deps eslint@8.57.1 eslint-plugin-security@1.7.1 eslint-plugin-no-unsanitized@4.1.5 htmlhint@1.9.2`

Letakkan source SUT di `sut/bizmart-umkm/` (atau set `SUT_DIR`), lalu jalankan:

    python -m pytest tests -v

Setiap test diberi nama `test_NFRxxx_...` sesuai ID di laporan Test Design Specification.
