"""Tests for storage implementations."""

import pytest
import tempfile
import json
from pathlib import Path
from ai_image_gen_mcp.storage.local import LocalStorage


@pytest.fixture
async def local_storage():
    """Create a temporary local storage instance."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = LocalStorage(Path(tmpdir))
        yield storage


@pytest.mark.asyncio
async def test_local_storage_save_and_get(local_storage):
    """Test saving and retrieving images from local storage."""
    # Test data
    test_data = b"test image data"
    filename = "test.png"
    metadata = {"prompt": "test prompt", "model": "test-model"}
    
    # Save image
    path = await local_storage.save(test_data, filename, metadata)
    
    # Verify path exists
    assert Path(path).exists()
    assert path.endswith(".png")
    
    # Retrieve image
    retrieved_data = await local_storage.get(path)
    assert retrieved_data == test_data
    
    # Check metadata was saved
    metadata_path = Path(path).with_suffix(".png.json")
    assert metadata_path.exists()
    with open(metadata_path) as f:
        saved_metadata = json.load(f)
    assert saved_metadata["prompt"] == "test prompt"


@pytest.mark.asyncio
async def test_local_storage_exists(local_storage):
    """Test checking if image exists."""
    # Save an image
    test_data = b"test"
    path = await local_storage.save(test_data, "test.png")
    
    # Check existence
    assert await local_storage.exists(path) is True
    assert await local_storage.exists("/nonexistent/path.png") is False


@pytest.mark.asyncio
async def test_local_storage_delete(local_storage):
    """Test deleting images from storage."""
    # Save an image with metadata
    test_data = b"test"
    metadata = {"test": "data"}
    path = await local_storage.save(test_data, "test.png", metadata)
    
    # Verify it exists
    assert await local_storage.exists(path) is True
    
    # Delete it
    result = await local_storage.delete(path)
    assert result is True
    
    # Verify it's gone
    assert await local_storage.exists(path) is False
    
    # Verify metadata is also gone
    metadata_path = Path(path).with_suffix(".png.json")
    assert not metadata_path.exists()


@pytest.mark.asyncio
async def test_local_storage_unique_filenames(local_storage):
    """Test that storage generates unique filenames."""
    # Save two images with same suggested filename
    data1 = b"image1"
    data2 = b"image2"
    
    path1 = await local_storage.save(data1, "same.png")
    path2 = await local_storage.save(data2, "same.png")
    
    # Paths should be different
    assert path1 != path2
    
    # Both should exist
    assert await local_storage.exists(path1) is True
    assert await local_storage.exists(path2) is True