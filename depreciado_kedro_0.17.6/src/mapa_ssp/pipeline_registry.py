"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from mapa_ssp.pipelines import raspagem


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    pipe_raspagem = raspagem.create_pipeline()

    return {"__default__": Pipeline([
        pipe_raspagem
    ])}
