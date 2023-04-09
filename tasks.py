from invoke import task, Collection

ns = Collection()


@task
def run_isort(c) -> None:
    """Run isort on source"""
    print("Running ISORT")
    print("-------------")
    c.run("isort --settings-path=./pyproject.toml src/", pty=True)
    print("Done")


@task
def run_black(c) -> None:
    """Run black code formatter on source"""
    print("Running BLACK")
    print("-------------")
    c.run("black --config=./pyproject.toml src/", pty=True)
    print("Done")


@task
def run_pylint(c) -> None:
    """Run pylint on source"""
    print("Running PYLINT")
    print("--------------")
    c.run("pylint --rcfile=./pyproject.toml src/", pty=True)
    print("Done")


@task
def run_mypy(c) -> None:
    """Run mypy type checking on source"""
    print("Running MYPY")
    print("------------")
    c.run("mypy --config-file=./pyproject.toml --check-untyped-defs src/", pty=True)
    print("Done")


@task
def run_all(c) -> None:
    """Run all code quality checks"""
    run_isort(c)
    run_black(c)
    run_pylint(c)
    run_mypy(c)


ns = Collection()
precheck = Collection("precheck")
precheck.add_task(run_pylint, "pylint")
precheck.add_task(run_mypy, "mypy")
precheck.add_task(run_black, "black")
precheck.add_task(run_isort, "isort")
precheck.add_task(run_all, "all")
ns.add_collection(precheck)
