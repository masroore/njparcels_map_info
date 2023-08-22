# Copyright 2023 Dr. Masroor Ehsan
from typing import Any

from scrape_kit.src.web.task import TaskRequest
from scrape_kit.src.web.worker import BaseWebWorker


class BatchedDownloader:
    _urls: list[str]
    _work_queue: list[str]
    _tasks: list[TaskRequest]
    _callback_fn: Any
    _workers: BaseWebWorker

    def __init__(self, workers: BaseWebWorker, concurrency: int):
        self._urls = []
        self._work_queue = []
        self._workers = workers
        self._tasks = []
        self._concurrency = concurrency

    @property
    def urls(self) -> list[str]:
        return self._urls

    @urls.setter
    def urls(self, urls: list[str]):
        self._urls = list(set([u for u in urls if u.strip()]))

    def reset(self):
        self._tasks = []

    def run(self):
        work_queue: list[str] = self._urls

        batch_count = 0
        while True:
            url = work_queue.pop()
            batch_count += 1
            item = TaskRequest(
                url=url, proxy_disabled=False, session_id="", session_disabled=True
            )
            self._tasks.append(item)

            if batch_count >= self._concurrency:
                self._workers.add_tasks(self._tasks)
                self._workers.run(reset_queue=True)
                batch_count = 0
                self.reset()

            if not any(work_queue):
                return
