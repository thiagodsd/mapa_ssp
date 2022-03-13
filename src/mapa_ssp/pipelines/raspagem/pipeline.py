"""
This is a boilerplate pipeline 'raspagem'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import baixa_csv


def create_pipeline(**kwargs):
    return Pipeline([
        node(
                baixa_csv,
                inputs=[
                    "params:ano_ini_index",
                    "params:ano_fim_index",
                    "params:del_ini_index",
                    "params:del_fim_index",
                    ],
                outputs=None,
                name="baixa_csv",
            )
    ])
