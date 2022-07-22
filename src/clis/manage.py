import actions
import click
from loguru import logger

from src.tasks.utils import import_string


@logger.catch
def init_cli() -> None:
    """
    - Care your naming module: if A module should have similar A_cli group clicks
    """
    # TODO: Add your click command
    for _state in actions.__all__:
        try:
            obj_cli = import_string(f"actions.{_state}.{_state}_cli")
            cli.add_command(obj_cli)
        except Exception as exc:
            fm_str = f"""###################################################################\n# Init {_state.upper()} have exception:                                    #\n###################################################################"""
            click.echo(fm_str)
            logger.error(exc)
            click.echo("\n")


@click.group()
def cli() -> None:
    pass


if __name__ == "__main__":
    init_cli()
    cli()
