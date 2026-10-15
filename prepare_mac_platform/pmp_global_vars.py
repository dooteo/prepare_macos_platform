
import os

#   .------------------------.
# --|   Global Variables     |
#   '------------------------'

HOME_DIR = os.path.expanduser('~')
DOWNLOADS_DIR = os.path.join(HOME_DIR, 'Downloads/prepare_mac_platform')
EXTRACT_DIR = os.path.join(DOWNLOADS_DIR, 'tmp_extract')
APPLICATIONS_DIR = "/Applications"
#VOLUME_DIR = "/tmp"
VOLUME_DIR = os.path.join(DOWNLOADS_DIR, 'tmp_volumes')

USER_AGENT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
    "refere": "https://example.com",
    "cookie": """your cookie value ( you can get that from your web page) """,
}
