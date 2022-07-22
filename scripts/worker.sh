#! /usr/bin/env bash
export PYTHONPATH=.
celery -A src.tasks.base worker -l info -c5
