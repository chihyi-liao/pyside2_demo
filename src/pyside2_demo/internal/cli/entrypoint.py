import click

from.examples import example_group


@click.group()
def entry_point():
    pass


# noinspection PyTypeChecker
entry_point.add_command(example_group)
