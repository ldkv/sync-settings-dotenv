from pathlib import Path
from typing import Annotated

import typer
from dotenv import dotenv_values
from rich import print as rprint

from sync_settings_dotenv.utils import generate_dotenv_file, generate_source_env_vars, resolve_env_vars_combination

app = typer.Typer(help="A CLI tool to sync environment variables in dotenv files or from Python settings files.")


@app.command()
def sync_settings_dotenv(
    src_path: Annotated[
        str,
        typer.Argument(
            ...,
            help="Full path to the module with environment variables to sync. It can be either an .env file or a Python module path containing a Pydantic BaseSettings subclass.",
        ),
    ],
    dst_path: Annotated[
        Path,
        typer.Argument(..., help="Output path for the generated .env file."),
    ] = Path(".env"),
    overwrite_values: bool = typer.Option(
        False,
        "--overwrite-values",
        help="Overwrite existing values in the .env file. Keep extra variables that are not in the source.",
    ),
    exact_match: bool = typer.Option(
        False,
        "--exact",
        help="Match the .env file exactly to the source. Remove any extra variables not present in the source.",
    ),
    with_header: bool = typer.Option(
        True,
        "--header/--no-header",
        help="Include a header comment in the .env file.",
    ),
):
    """
    Sync environment variables from a source to a target .env file.

    The function generates or updates the target .env file based on the source, with options to overwrite values or exact match.
    """
    try:
        src_env_vars = generate_source_env_vars(src_path)
    except ImportError as e:
        rprint(f"[red]Error:[/red] Unable to import settings model from {src_path=}. Error: {e}")
        raise typer.Exit(code=1) from e

    dst_env_vars = dotenv_values(dst_path)
    combined_env_vars = resolve_env_vars_combination(
        src_env_vars,
        dst_env_vars,
        overwrite_values=overwrite_values,
        exact_match=exact_match,
    )
    if combined_env_vars == dst_env_vars:
        rprint("[blue]Info:[/blue] No changes detected. Skipping update.")
        return

    generate_dotenv_file(dst_path, combined_env_vars, with_header=with_header)
    rprint(f"[green]Success:[/green] Generated .env file at '{dst_path}'.")


if __name__ == "__main__":
    app()
