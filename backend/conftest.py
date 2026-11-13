"""Shared pytest fixtures for the whole backend."""
import pytest


@pytest.fixture(autouse=True)
def temporary_media(settings, tmp_path):
    """Uploaded and seeded files go to a temporary folder, never to the real backend/media/."""
    settings.MEDIA_ROOT = tmp_path / "media"
    return settings.MEDIA_ROOT
