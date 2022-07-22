#! /usr/bin/env bash
export PYTHONPATH=.
celery -A src.tasks.base beat -l info
