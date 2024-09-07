""""download bing UHD wallpapers
- Wei Du
"""

import glob
import os

import requests


def get_local_files(p: str) -> list:
    files: list[str] = glob.glob(p + "/*")
    files: list[str] = [os.path.basename(x) for x in files]

    return files


def get_online_files(url: str) -> tuple[list, list]:
    text: str = requests.get(url).text
    # text: str = requests.get(url, verify = False).text
    lines: list[str] = text.split("\n")
    lines: list[str] = [line.strip() for line in lines]  # remove ending \n
    lines: list[str] = [line for line in lines if line.strip()]  # remove empty lines
    lines: list[str] = lines[1:]  # remove 1st line

    urls: list[str] = [line.split("]")[1][1:-1] for line in lines]
    urls: list[str] = [line.split("&")[0] if "&" in line else line for line in urls]
    files: list[str] = [url.rsplit("/", 1)[1][6:] for url in urls]

    return urls, files


def diff_files(loc_files: list, files: list, urls: list) -> tuple[list, list]:
    new_files: list[str] = []
    new_urls: list[str] = []

    for i, file in enumerate(files):
        if file not in loc_files:
            new_files.append(file)
            new_urls.append(urls[i])

    return new_urls, new_files


def download(files: list, urls: list, p: str) -> None:
    n_files: int = len(files)

    if n_files > 0:
        for i, file in enumerate(files):
            r = requests.get(urls[i])

            open(os.path.join(p, file), "wb").write(r.content)

            print("{}/{}, {} ...".format(i + 1, n_files, file))

    else:
        print("no new files to download")

    print()
    print("DONE")


# loc_path: str = '/Users/v/Pictures/bing-wallpapers'
loc_path: str = "/Users/v/Library/CloudStorage/OneDrive-Personal/图片/必应壁纸"

url_en: str = (
    "https://raw.githubusercontent.com/niumoo/bing-wallpaper/main/bing-wallpaper.md"
)
url_cn: str = (
    "https://raw.githubusercontent.com/niumoo/bing-wallpaper/main/zh-cn/bing-wallpaper.md"
)

loc_files: list[str] = get_local_files(loc_path)
n_loc_files: int = len(loc_files)
print()
print("local files  : {} ".format(n_loc_files))

urls_en, files_en = get_online_files(url_en)
n_online_files_en: int = len(files_en)

urls_cn, files_cn = get_online_files(url_cn)
n_online_files_cn: int = len(files_cn)
print()
print("online files : {} ".format(n_online_files_en + n_online_files_cn))
print("          EN : {} ".format(n_online_files_en))
print("          CN : {} ".format(n_online_files_cn))

urls: list[str] = urls_en + urls_cn
files: list[str] = files_en + files_cn

new_urls, new_files = diff_files(loc_files, files, urls)
n_new_files: int = len(new_files)
print()
print("new files    : {} ".format(n_new_files))
print()

new_urls: list[str] = new_urls[::-1]
new_files: list[str] = new_files[::-1]

download(new_files, new_urls, loc_path)
