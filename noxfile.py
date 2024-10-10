import os

import nox

nox.options.default_venv_backend = "uv"


@nox.session()
def lint(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--extra=lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    LINT_PATHS = ("src/trustme", "tests", "noxfile.py")
    session.run("black", *LINT_PATHS)
    session.run("isort", "--profile", "black", *LINT_PATHS)
    session.run("mypy", *LINT_PATHS)


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13", "pypy3.10"])
def test(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--extra=test",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run(
        "coverage",
        "run",
        "--parallel-mode",
        "-m",
        "pytest",
        "-W",
        "error",
        "-ra",
        "-s",
        *(session.posargs or ("tests/",)),
    )
    if os.environ.get("CI") != "true":
        session.run("coverage", "combine")
        session.run("coverage", "report", "-m")
