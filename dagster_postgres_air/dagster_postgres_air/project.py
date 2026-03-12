from pathlib import Path

import os
from dagster_dbt import DbtProject

os.environ["PATH"] = "/Library/Frameworks/Python.framework/Versions/3.13/bin:" + os.environ["PATH"]
my_dbt_project_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "DBT").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
my_dbt_project_project.prepare_if_dev()