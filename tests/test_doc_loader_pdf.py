import importlib.util
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOADER_PATHS = [
    ROOT / "company-research" / "scripts" / "doc_loader.py",
    ROOT / "critical-questions" / "scripts" / "doc_loader.py",
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_text_pdf(path: Path, text: str):
    import pymupdf

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=12)
    doc.save(path)
    doc.close()


@pytest.fixture
def fake_tesseract_install(tmp_path):
    install_dir = tmp_path / "Tesseract-OCR"
    tessdata_dir = install_dir / "tessdata"
    tessdata_dir.mkdir(parents=True)
    tesseract_cmd = install_dir / "tesseract.exe"
    tesseract_cmd.write_text("", encoding="utf-8")
    (tessdata_dir / "chi_sim.traineddata").write_text("", encoding="utf-8")
    (tessdata_dir / "eng.traineddata").write_text("", encoding="utf-8")
    return install_dir, tesseract_cmd


@pytest.mark.parametrize("loader_path", LOADER_PATHS, ids=lambda p: p.parts[-3])
def test_configure_tesseract_uses_windows_registry_install_dir(
    loader_path, fake_tesseract_install, monkeypatch
):
    install_dir, tesseract_cmd = fake_tesseract_install
    doc_loader = load_module(loader_path, f"doc_loader_registry_{loader_path.parts[-3].replace('-', '_')}")

    class FakeWinreg:
        HKEY_LOCAL_MACHINE = object()
        HKEY_CURRENT_USER = object()
        KEY_READ = 0
        KEY_WOW64_64KEY = 0
        KEY_WOW64_32KEY = 0

        def OpenKey(self, root, subkey, *args):
            return self

        def QueryValueEx(self, key, value_name):
            if value_name == "InstallDir":
                return str(install_dir), None
            raise FileNotFoundError(value_name)

        def CloseKey(self, key):
            pass

    fake_pytesseract = types.SimpleNamespace(
        pytesseract=types.SimpleNamespace(tesseract_cmd="tesseract")
    )

    monkeypatch.delenv("TESSERACT_CMD", raising=False)
    monkeypatch.setattr(doc_loader.shutil, "which", lambda name: None)
    monkeypatch.setitem(sys.modules, "winreg", FakeWinreg())
    monkeypatch.setitem(sys.modules, "pytesseract", fake_pytesseract)

    resolved = doc_loader.configure_tesseract()

    assert resolved == tesseract_cmd
    assert fake_pytesseract.pytesseract.tesseract_cmd == str(tesseract_cmd)
    assert doc_loader.get_ocr_lang(tesseract_cmd) == "chi_sim+eng"


@pytest.mark.parametrize("loader_path", LOADER_PATHS, ids=lambda p: p.parts[-3])
def test_embedded_text_pdf_is_read_with_ocr(loader_path, tmp_path, monkeypatch):
    sample_text = "OCR text from rendered PDF page."
    pdf_path = tmp_path / "embedded-text.pdf"
    make_text_pdf(pdf_path, "PDF text layer that should be ignored by OCR.")

    import pytesseract

    ocr_calls = []

    def fake_image_to_string(*args, **kwargs):
        ocr_calls.append(kwargs)
        return sample_text

    monkeypatch.setattr(pytesseract, "image_to_string", fake_image_to_string)
    monkeypatch.setattr(pytesseract, "get_tesseract_version", lambda: "5.4.0")
    module_name = f"doc_loader_{loader_path.parts[-3].replace('-', '_')}"
    sys.modules.pop(module_name, None)
    doc_loader = load_module(loader_path, module_name)
    monkeypatch.setattr(doc_loader, "configure_tesseract", lambda: Path("tesseract.exe"))
    monkeypatch.setattr(doc_loader, "get_ocr_lang", lambda cmd=None: "chi_sim+eng")

    result = doc_loader.process_pdf(pdf_path, tmp_path, max_pages=5)

    assert ocr_calls
    assert ocr_calls[0]["lang"] == "chi_sim+eng"
    assert result["pdf_type"] == "text_based"
    assert result["content_type"] == "pdf_ocr"
    assert sample_text in result["content"]
    assert Path(result["ocr_path"]).exists()
    assert result["content_length"] == len(result["content"])
