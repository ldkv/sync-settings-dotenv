from pathlib import Path
from typing import Annotated, Type

import typer
from dotenv import dotenv_values
from pydantic_settings import BaseSettings
from rich import print as rprint

from sync_settings_dotenv.utils import generate_dotenv_file, import_class_from_module, serialize_default_env_vars


def update_env_file(settings_model: Type[BaseSettings], env_path: Path, overwrite: bool = False) -> None:
    env_vars = dotenv_values(env_path)
    overwritten_keys = set()
    for field_name, default_value in serialize_default_env_vars(settings_model).items():
        field_name_upper = field_name.upper()
        if not overwrite and field_name_upper in env_vars:
            continue

        existing_value = env_vars.get(field_name_upper)
        if existing_value != default_value:
            overwritten_keys.add(field_name_upper)

        env_vars[field_name_upper] = default_value

    if not overwritten_keys:
        rprint("[blue]Info:[/blue] No environment variables were overwritten.")
        return

    generate_dotenv_file(env_path, env_vars)


def sync_settings_dotenv(
    module_path: str = typer.Argument(..., help="Full path to the module containing the Pydantic BaseSettings model."),
    env_path: Annotated[
        Path,
        typer.Option(
            ".env",
            "--output",
            "-o",
            help="Output path for the generated .env file.",
        ),
    ] = Path(".env"),
    overwrite_values: bool = typer.Option(
        False,
        "--overwrite-values",
        help="Overwrite existing values in the .env file.",
    ),
):
    """Generate an .env file from a Pydantic BaseSettings model."""
    try:
        settings_model = import_class_from_module(module_path)
    except ImportError as e:
        rprint(f"[red]Error:[/red] Unable to import settings model from {module_path=}. Error: {e}")
        raise typer.Exit(code=1) from e

    update_env_file(settings_model, env_path, overwrite=overwrite_values)
    rprint(f"[green]Success:[/green] Generated .env file at '{env_path}'.")


def main():
    typer.run(sync_settings_dotenv)


if __name__ == "__main__":
    main()
