import os
import subprocess

# TODO: set dir import back to root dir
import sys
from typing import Optional

import click
from click import Group

sys.path.append(os.path.abspath(os.getcwd()))

from src.app.core.config import constants, secrets


def init() -> Group:
    app_dir = os.path.dirname(os.path.dirname(__file__))
    if not os.path.exists(f"{app_dir}/..{constants.DB_LOCATION[1:]}"):
        os.makedirs(f"{app_dir}/..{constants.DB_LOCATION[1:]}")
    return Group("init_db", help="Cli for init db")


init_db_cli = init()


@init_db_cli.command("new", help="New commit for database")
@click.option(
    "-m",
    "--message",
    nargs=1,
    type=click.STRING,
    help="Message for this commit",
    required=True,
)
def new(message: str) -> None:
    """
    Create new commit for database
    """
    message = message.replace(" ", "-")
    cmd = f"yoyo new {constants.DB_LOCATION} -m {message} -b --no-config"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()


@init_db_cli.command("upgrade", help="Upgrade db to the newest")
@click.option(
    "-i",
    "--id",
    nargs=1,
    type=click.STRING,
    help="Id to upgrade DB",
)
def upgrade(id: Optional[str] = None) -> None:
    """
    Upgrade Database
    """
    click.echo("Begin upgrade database")
    if id is None:
        cmd = f"yoyo apply --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} --all --no-config -b"
    else:
        cmd = f"yoyo apply --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} -r {id} --no-config -b"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()


@init_db_cli.command("rollback", help="Rollback db to the previous commit")
@click.option(
    "-i",
    "--id",
    nargs=1,
    type=click.STRING,
    help="Id to rollback DB",
)
def rollback(id: Optional[str] = None) -> None:
    """
    Rollback Database
    """
    click.echo("Rollback database")
    if id is None:
        cmd = f"yoyo rollback --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} --all --no-config -b"
    else:
        cmd = f"yoyo rollback --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} -r {id} --no-config -b"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()


@init_db_cli.command("list", help="List commit migration in db")
def list_commit() -> None:
    """
    List commit
    """
    cmd = f"yoyo list --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} --no-config -b"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()


@init_db_cli.command("reapply", help="Reapply commit migration in db")
@click.option(
    "-i",
    "--id",
    nargs=1,
    type=click.STRING,
    help="Id to reapply DB",
)
def reapply(id: Optional[str] = None) -> None:
    """
    Reapply commit
    """
    if id is None:
        cmd = f"yoyo reapply --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} --all --no-config -b"
    else:
        cmd = f"yoyo reapply --database {secrets.DB_POSTGRES_DSN} {constants.DB_LOCATION} -r {id} --no-config -b"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()


@init_db_cli.command("break-lock", help="Break lock db")
def break_lock() -> None:
    """
    Break lock Database
    """
    cmd = f"yoyo break-lock --database {secrets.DB_POSTGRES_DSN} --no-config -b"
    cmd_exec = subprocess.Popen(cmd, shell=True)
    cmd_exec.wait()
