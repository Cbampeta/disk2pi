import os
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image
import numpy as np
from PyPDF2 import PdfWriter

from utils import Utils
from utils import ImageUtils
from utils import PDFUtils


@pytest.fixture
def sample_png(tmp_path):
    path = tmp_path / "sample.png"
    img = Image.new("RGBA", (10, 20), (255, 0, 0, 255))
    img.save(path)
    return path


@pytest.fixture
def sample_rgb_png(tmp_path):
    path = tmp_path / "rgb.png"
    img = Image.new("RGB", (10, 10), (100, 150, 200))
    img.save(path)
    return path


def test_creer_dossier_cree_un_dossier(tmp_path):
    dossier = tmp_path / "nouveau"

    Utils.creer_dossier(dossier)

    assert dossier.exists()
    assert dossier.is_dir()


def test_creer_fichier_cree_un_fichier(tmp_path):
    fichier = tmp_path / "test.txt"

    Utils.creer_fichier(fichier)

    assert fichier.exists()
    assert fichier.read_text() == ""


def test_changer_extension():
    assert Utils.changer_extension("image.png", "jpg") == "image.jpg"


def test_conversion_png_to_jpeg(sample_png, tmp_path):
    output = tmp_path / "converted.jpeg"

    with (
        patch.object(Utils, "output_file_name", return_value=str(output)),
        patch.object(Utils, "creer_fichier"),
        patch.object(Utils, "open_output_file"),
    ):
        result = ImageUtils.conversion(str(sample_png), "jpeg")

    assert result == str(output)
    assert output.exists()

    img = Image.open(output)
    assert img.format == "JPEG"
    assert img.mode == "RGB"


def test_conversion_to_pdf_calls_open_output_file(sample_rgb_png, tmp_path):
    output = tmp_path / "converted.pdf"

    with (
        patch.object(Utils, "output_file_name", return_value=str(output)),
        patch.object(Utils, "creer_fichier"),
        patch.object(Utils, "open_output_file") as mock_open,
    ):
        result = ImageUtils.conversion(str(sample_rgb_png), "pdf")

    assert result == str(sample_rgb_png)  # <- changé ici
    assert output.exists()
    mock_open.assert_called_once_with(str(output))


def test_rotate_image_90_degres(sample_rgb_png, tmp_path):
    output = tmp_path / "rotated.png"

    with patch.object(Utils, "output_file_name", return_value=str(output)):
        result = ImageUtils.rotate(str(sample_rgb_png), angle=90)

    assert result == str(output)
    assert output.exists()

    img = Image.open(output)
    assert img.size == (10, 10)


def test_rotate_image_change_dimensions(tmp_path):
    src = tmp_path / "rect.png"
    Image.new("RGB", (10, 20), (255, 0, 0)).save(src)

    output = tmp_path / "rotated.png"

    with patch.object(Utils, "output_file_name", return_value=str(output)):
        ImageUtils.rotate(str(src), angle=90)

    img = Image.open(output)
    assert img.size == (20, 10)


def test_negate_image(sample_rgb_png, tmp_path):
    output = tmp_path / "negated.png"

    with patch.object(Utils, "output_file_name", return_value=str(output)):
        result = ImageUtils.negate_image(str(sample_rgb_png))

    assert result == str(output)

    img = Image.open(output)
    pixel = img.getpixel((0, 0))

    assert pixel == (155, 105, 55)


def test_detect_bg_color():
    data = np.zeros((4, 4, 4), dtype=np.uint8)

    data[0, 0, :3] = [250, 250, 250]
    data[0, -1, :3] = [255, 255, 255]
    data[-1, 0, :3] = [248, 248, 248]
    data[-1, -1, :3] = [10, 10, 10]

    bg = ImageUtils.detect_bg_color(data)

    assert np.array_equal(bg, np.array([240, 240, 240]))


def test_remove_background(tmp_path):
    src = tmp_path / "bg.png"

    img = Image.new("RGBA", (5, 5), (255, 255, 255, 255))
    img.putpixel((2, 2), (255, 0, 0, 255))
    img.save(src)

    output = tmp_path / "removed.png"

    with patch.object(Utils, "output_file_name", return_value=str(output)):
        result = ImageUtils.remove(str(src), tolerance=30)

    assert result == str(output)

    result_img = Image.open(output).convert("RGBA")

    assert result_img.getpixel((0, 0))[3] == 0
    assert result_img.getpixel((2, 2))[3] == 255


def test_compress_png_creates_jpeg_file(sample_rgb_png, tmp_path):
    output = tmp_path / "compressed.png"

    with (
        patch.object(Utils, "output_file_name", return_value=str(output)),
        patch.object(Utils, "creer_fichier"),
    ):
        result = ImageUtils.compress(str(sample_rgb_png), quality=50)

    expected_output = tmp_path / "compressed.jpg"

    assert result == str(expected_output)
    assert expected_output.exists()

    img = Image.open(expected_output)
    assert img.format == "JPEG"


def test_pdf_to_txt_empty_pdf(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    txt_path = tmp_path / "output.txt"

    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    with open(pdf_path, "wb") as f:
        writer.write(f)

    with (
        patch.object(Utils, "output_file_name", return_value=str(txt_path)),
        patch.object(Utils, "creer_fichier"),
    ):
        result = PDFUtils.pdf_to_txt(str(pdf_path))

    assert result == str(txt_path)
    assert txt_path.exists()
    assert txt_path.read_text(encoding="utf-8") == ""
