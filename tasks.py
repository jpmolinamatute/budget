from pathlib import Path
from invoke import task, Collection
from invoke.context import Context

ns = Collection()

PROJECT_DIR = Path(__file__).parent.absolute()


def __isort(ctx: Context) -> None:
    """Run isort on source"""
    print("Running ISORT")
    print("-------------")
    ctx.run(f"isort --settings-path={PROJECT_DIR}/pyproject.toml {PROJECT_DIR}/src")
    print("Done")


def __black(ctx: Context) -> None:
    """Run black code formatter on source"""
    print("Running BLACK")
    print("-------------")
    ctx.run(f"black --config={PROJECT_DIR}/pyproject.toml {PROJECT_DIR}/src")
    print("Done")


def __pylint(ctx: Context) -> None:
    """Run pylint on source"""
    print("Running PYLINT")
    print("--------------")
    ctx.run(f"pylint --rcfile={PROJECT_DIR}/pyproject.toml {PROJECT_DIR}/src")
    print("Done")


def __mypy(ctx: Context) -> None:
    """Run mypy type checking on source"""
    print("Running MYPY")
    print("------------")
    ctx.run(f"mypy --config-file={PROJECT_DIR}/pyproject.toml {PROJECT_DIR}/src")
    print("Done")


@task
def run_isort(ctx: Context) -> None:
    __isort(ctx)


@task
def run_black(ctx: Context) -> None:
    __black(ctx)


@task
def run_pylint(ctx: Context) -> None:
    __pylint(ctx)


@task
def run_mypy(ctx: Context) -> None:
    __mypy(ctx)


@task
def run_all(ctx: Context) -> None:
    """Run all code quality checks"""
    __isort(ctx)
    __black(ctx)
    __pylint(ctx)
    __mypy(ctx)


ns = Collection()
precheck = Collection("precheck")
precheck.add_task(run_pylint, "pylint")
precheck.add_task(run_mypy, "mypy")
precheck.add_task(run_black, "black")
precheck.add_task(run_isort, "isort")
precheck.add_task(run_all, "all")
ns.add_collection(precheck)
