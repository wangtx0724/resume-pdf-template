"""Install the official Alibaba PuHuiTi 3.0 package into this skill's local cache."""

from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "assets" / "fonts"
ARCHIVE = CACHE / "AlibabaPuHuiTi-3.zip"
FONT_DIR = CACHE / "AlibabaPuHuiTi-3"
URL = "https://fonts.alibabadesign.com/AlibabaPuHuiTi-3.zip"


def main():
    if (FONT_DIR / "AlibabaPuHuiTi-3-55-Regular" / "AlibabaPuHuiTi-3-55-Regular.ttf").is_file():
        print(FONT_DIR)
        return

    CACHE.mkdir(parents=True, exist_ok=True)
    request = Request(
        URL,
        headers={
            "Referer": "https://www.alibabafonts.com/",
            "Origin": "https://www.alibabafonts.com",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urlopen(request) as response, ARCHIVE.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)

    with ZipFile(ARCHIVE) as package:
        package.extractall(CACHE)
    ARCHIVE.unlink()
    print(FONT_DIR)


if __name__ == "__main__":
    main()
