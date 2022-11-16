"""
Tests the basic loading and storage of an image w/ Photoshop
"""
import os
import shutil
import time

import pytest
from scistag.common.test_data import TestConstants
from scistag.imagestag import Image
from scistag.webstag import web_fetch

from photoshop import api as ps
from psd_tools import PSDImage


def test_open_and_load():
    """
    Loads an image provided from SciStag, stores it w/ Photoshop and verified it
    :return:
    """
    os.makedirs("./temp_in", exist_ok=True)
    try:
        shutil.rmtree("./temp_out")
    except FileNotFoundError:
        pass
    os.makedirs("./temp_out", exist_ok=True)
    temp_image_path = "./temp_in/test_image.jpg"
    out_path = os.path.abspath("./temp_out/test_out.bmp").replace("\\", "/")
    if not os.path.exists(temp_image_path):
        web_fetch(TestConstants.STAG_URL, filename=temp_image_path)
    full_path = os.path.abspath(temp_image_path)

    app = ps.Application()
    for doc in app.documents:
        doc.close()

    app.open(full_path)
    doc = app.activeDocument
    doc.saveAs(file_path=out_path, options=ps.BMPSaveOptions(), asCopy=True)

    image = Image(out_path)
    assert image.size == (665, 525)
    mean = image.get_pixels().mean()
    assert mean == pytest.approx(122.84, 0.05)
