# """Project pipelines."""
# from __future__ import annotations

# from kedro.framework.project import find_pipelines
# from kedro.pipeline import Pipeline


# def register_pipelines() -> dict[str, Pipeline]:
#     """Register the project's pipelines.

#     Returns:
#         A mapping from pipeline names to ``Pipeline`` objects.
#     """
#     pipelines = find_pipelines()
#     pipelines["__default__"] = sum(pipelines.values())
#     return pipelines


"""Project pipelines."""
from __future__ import annotations
from typing import Dict
from kedro.framework.project import find_pipelines
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
