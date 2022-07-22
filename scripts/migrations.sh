#! /usr/bin/env bash
export PYTHONPATH=.
python src/clis/manage.py init_db "$@"
