from typing import List

from celery import Celery
from celery.schedules import crontab
from pydantic import BaseSettings

from src.app.core.config import secrets


class TaskService:
    __instance__ = None

    class CelerySettings(BaseSettings):
        task_result_expires: int = 600
        timezone: str = "Asia/Ho_Chi_Minh"
        accept_content: List[str] = ["json", "msgpack", "yaml"]
        task_serializer: str = "json"
        result_serializer: str = "json"
        ignore_result: bool = False
        track_started: bool = True
        task_track_started: bool = True
        result_extended: bool = True
        imports: list = ["src.tasks.job", "src.tasks.cron", "src.app.services.am_ads"]

    @classmethod
    def init_celery(cls) -> None:
        cls.__instance__ = Celery(
            "worker",
            broker=secrets.AMPQ_DSN,
            backend=secrets.REDIS_DSN,
        )
        cls.celery_conf()
        cls.celery_beat_schedule()

    @classmethod
    def celery_conf(cls) -> None:
        if cls.__instance__ is None:
            raise (cls.NoneInstanceExc("Instance Celery not found"))
        cls.__instance__.conf.update(cls.CelerySettings())

    @classmethod
    def celery_beat_schedule(cls):
        if cls.__instance__ is None:
            raise (cls.NoneInstanceExc("Instance Celery not found"))
        cls.__instance__.conf.beat_schedule = {
            # INSTRUCTION:
            # "test-every-10-sec": {
            #     "task": "app.services.tasks.cron.test_every_10_sec",
            #     "schedule": 10.0,
            #     "args": (),
            #     "kwargs": {},
            # },
            #  "test-every-at-0h": {
            #     "task": "app.services.tasks.cron.test_every_at_0h",
            #     "schedule": crontab(hour=0, minute=1),
            #     "args": (),
            #     "kwargs": {},
            # },
            ############################################################
        }

    @classmethod
    def get_instance(cls):
        if cls.__instance__ == None:
            cls.init_celery()
        return cls.__instance__

    class CeleryException(Exception):
        pass

    class NoneInstanceExc(CeleryException):
        pass


task_service = TaskService.get_instance()
