from invoke import task, Collection
from invoke.context import Context

ns = Collection()


def __isort(ctx: Context) -> None:
    """Run isort on source"""
    print("Running ISORT")
    print("-------------")
    ctx.run("isort --settings-path=./pyproject.toml src/", pty=True)
    print("Done")


def __black(ctx: Context) -> None:
    """Run black code formatter on source"""
    print("Running BLACK")
    print("-------------")
    ctx.run("black --config=./pyproject.toml src/", pty=True)
    print("Done")


def __pylint(ctx: Context) -> None:
    """Run pylint on source"""
    print("Running PYLINT")
    print("--------------")
    ctx.run("pylint --rcfile=./pyproject.toml src/", pty=True)
    print("Done")


def __mypy(ctx: Context) -> None:
    """Run mypy type checking on source"""
    print("Running MYPY")
    print("------------")
    ctx.run("mypy --config-file=./pyproject.toml --check-untyped-defs src/", pty=True)
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
