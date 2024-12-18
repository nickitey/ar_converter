import os

from src.presentation.app import app, settings

workdir = settings.common_app.workdir
if not os.path.isdir(workdir):
    os.mkdir(workdir)

os.chdir(workdir)


__all__ = ("app",)
