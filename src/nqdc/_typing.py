"""Base classes and utilities for typing."""
from os import PathLike
from pathlib import Path
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
import argparse
from typing import Union, Dict, Any, Tuple, Mapping, Optional

from lxml import etree
import pandas as pd

try:
    from nilearn import maskers
# import only used for type annotations, was called input_data in old nilearn
# versions
except ImportError:  # pragma: nocover
    from nilearn import input_data as maskers


NiftiMasker = maskers.NiftiMasker

PathLikeOrStr = Union[PathLike, str]
# argparse public functions (add_argument_group) return a private type so we
# have to use it here.
# pylint: disable-next=protected-access
ArgparseActions = Union[argparse.ArgumentParser, argparse._ArgumentGroup]


class Extractor(ABC):
    """Extractors used by the `_data_extraction` module."""

    @property
    @abstractmethod
    def fields(self) -> Tuple[str, ...]:
        """Return Dict keys or DataFrame columns produced by this extractor."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name for this extractor."""

    @abstractmethod
    def extract(
        self, article: etree.ElementTree
    ) -> Union[Dict[str, Any], pd.DataFrame]:
        """Extract data from an article."""


class Writer(AbstractContextManager):
    """Writers used by the `_data_extraction` module."""

    @abstractmethod
    def write(self, all_data: Mapping[str, Any]) -> None:
        """Write part of data extracted from article to storage."""


class Command:
    """An `nqdc` subcommand."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name for this command."""

    @property
    @abstractmethod
    def short_description(self) -> str:
        """A short description of the command."""

    @abstractmethod
    def edit_argument_parser(self, argument_parser: ArgparseActions) -> None:
        """Add arguments needed by this command to parser."""

    @abstractmethod
    def run(
        self,
        args: argparse.Namespace,
    ) -> int:
        """Execute this command. Return exit code."""


class PipelineStep:
    """An individual step in the `nqdc` pipeline (`nqdc run`)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name for this step."""

    @property
    @abstractmethod
    def short_description(self) -> str:
        """A short description of the processing step."""

    @abstractmethod
    def edit_argument_parser(self, argument_parser: ArgparseActions) -> None:
        """Add arguments needed by this step to parser."""

    @abstractmethod
    def run(
        self,
        args: argparse.Namespace,
        previous_steps_output: Mapping[str, Path],
    ) -> Tuple[Optional[Path], int]:
        """Execute this step. Return resulting directory and exit code."""


class StopPipeline(Exception):
    """Raised to indicate subsequent steps should not run."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
