# Copyright 2023 Dr. Masroor Ehsan
import glob
import os.path

import orjson as json
import yarl

from scrape_kit.src import utils
from scrape_kit.src.proxies import RotatingProxyPool
from scrape_kit.src.sessions import SessionManager
from scrape_kit.src.timer import Timer
from scrape_kit.src.web.task import TaskResult
from scrape_kit.src.web.worker import AsyncWebWorker
from batch_loader import BatchedDownloader
from localdb import PropertyInfo, init_db

APNS_TO_SCRAPE = utils.fget_lines("./apns.txt")
OUTPUT_FOLDER = os.path.abspath("./storage/njparcels/")
ALL_DATA = []


def urls_to_scrape(apns: list[str]) -> list[str]:
    urls = []
    for apn in apns:
        url = (
            f"https://cache.njparcels.com/attributes/v1.0/nj/{apn}?owner=1&assessment=1"
        )
        urls.append(url)
    return urls


def process_json_object(data: dict, apn: str):
    row = PropertyInfo.create(**data)
    return
    utils.fputb(
        f"{OUTPUT_FOLDER}/{apn}.json", json.dumps(data, option=json.OPT_SORT_KEYS)
    )


def handle_downloaded_resource(response: TaskResult, _: AsyncWebWorker):
    global timer
    apn = yarl.URL(response.url).name

    if response.is_error or response.status_code not in [200, 404]:
        utils.croak(
            f"{apn} HTTP {response.status_code}: {response.status_reason}",
            timer,
        )
        if response.exception:
            utils.croak(response.exception, timer)
        return

    if response.content:
        data = json.loads(response.content)
        process_json_object(data, apn)

    utils.croak(
        f"T: {response.elapsed_time:.1f} | HTTP {response.status_code} | DL: {response.content_length:<6} | {apn}",
        timer=timer,
    )


def check_apns() -> list[str]:
    checked = []
    files = [os.path.basename(x) for x in glob.glob(OUTPUT_FOLDER + "/*.json")]

    for apn in APNS_TO_SCRAPE:
        if apn not in files:
            checked.append(apn)

    return checked


if __name__ == "__main__":
    init_db()
    concurrency = 100
    timer: Timer = Timer()
    sessions: SessionManager = SessionManager()
    proxies: RotatingProxyPool = RotatingProxyPool(
        "p.webshare.io:80:qxerhmfs-rotate:odvgwubmbjti",
        concurrency=concurrency,
    )
    # print(proxies.pick());exit(0)
    workers: AsyncWebWorker = AsyncWebWorker(concurrency, proxies, sessions, timer)
    workers.set_result_available_hook(handle_downloaded_resource)

    loader = BatchedDownloader(workers=workers, concurrency=concurrency)
    utils.croak("Checking APNs...")
    apns = check_apns()
    utils.croak("Generating URLs...")
    loader.urls = urls_to_scrape(apns)
    timer.start()
    loader.run()
