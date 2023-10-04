"""
This is a boilerplate pipeline 'raspagem'
generated using Kedro 0.18.13
"""

from kedro.pipeline import Pipeline, node
from .nodes import download_data, data_aggregation

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
                download_data,
                inputs=[
                    "params:year_start_index",
                    "params:year_end_index",
                    "params:pol_station_start_index",
                    "params:pol_station_end_index",
                    ],
                outputs="download_data_status",
                name="download_data",
            ),
        node(
                data_aggregation,
                inputs=[
                    "params:year_start_index",
                    "params:year_end_index",
                    "download_data_status"
                    ],
                outputs="ssp_data",
                name="data_aggregation",
            ),
    ])

