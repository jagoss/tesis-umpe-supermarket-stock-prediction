"""Data repository adapters implementing ``DataRepositoryPort``.

Public API
----------
ParquetDataRepository
"""

from server.infrastructure.data.parquet_repository import ParquetDataRepository

__all__ = [
    "ParquetDataRepository",
]
