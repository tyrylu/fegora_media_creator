import requests
import logging

ZIPPED_IMAGE_URL = "https://cloud.vojtapolasek.eu/index.php/s/tA5KDZwTFwN8jz2/download?path=%2F&files=image.zip"
ZIPPED_IMAGE_MD5_URL = "https://cloud.vojtapolasek.eu/index.php/s/tA5KDZwTFwN8jz2/download?path=%2F&files=image.zip.md5"

session = requests.Session()

def download_image(local_path, progress_callback=None):
    resp = session.get(ZIPPED_IMAGE_URL, stream=True)
    if resp.status_code == 200:
        total = int(resp.headers.get("content-length", 0))
        chunk_size = 32*1024
        fp = local_path.open("wb")
        so_far = 0
        for chunk in resp.iter_content(chunk_size):
            so_far += len(chunk)
            fp.write(chunk)
            if progress_callback:
                progress_callback(total, so_far)
        fp.close()
        return True
    else:
        log.warn("Non 200 status code during image download: %s.", resp.status_code)
        return False

def get_image_checksum():
    resp = session.get(ZIPPED_IMAGE_MD5_URL)
    if resp.status_code == 200:
        return resp.text
    else:
        log.warn("Non 200 status during MD5 sum retrieval: %s", resp.status_code)
        return None