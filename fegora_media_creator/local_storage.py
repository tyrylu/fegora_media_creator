from pathlib import Path

IMAGE_CHECKSUM_FILE = Path("image.zip.md5")
IMAGE_FILE = Path("image.zip")

def image_checksum_is_current(server_checksum):
    if IMAGE_CHECKSUM_FILE.exists():
        local_checksum = IMAGE_CHECKSUM_FILE.read_text()
        return local_checksum == server_checksum
    return False # Checksum file not found

    def update_image_checksum(new_checksum):
        IMAGE_CHECKSUM_FILE.write_text(new_checksum)