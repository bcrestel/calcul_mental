from pathlib import Path
import logging

import numpy as np
import pandas as pd

from src.constants import Operation, file_path

logger = logging.getLogger(__name__)

class SummaryFile:
    def __init__(self, user_name: str, operation_type: Operation):
        self.user_name = user_name.lower()
        self.operation_type = operation_type
        logger.debug(f"operation_type={self.operation_type}")
        if not self.file_name.exists():
            logger.info(f"Could not find {self.file_name}. Creating default one")
            self._create_file(self.operation_type, self.file_name)
        logger.info(f"Loading {self.file_name}")
        self.df = pd.read_parquet(self.file_name)
        self.df_sampled = None


    @property
    def file_name(self):
        return Path(file_path, f"{self.user_name}_{self.operation_type.name}.parquet")


    @staticmethod
    def _create_file(operation_type: Operation, file_name: Path):
        if operation_type != Operation.division:
            a = (np.ones((12, 1)) * np.linspace(1, 12, 12)).flatten()
            b = (np.linspace(1, 12, 12, dtype=int).reshape((12, 1)) * np.ones(12)).flatten()
            df = pd.DataFrame({"a": a, "b": b}, dtype=int)
            if operation_type == Operation.addition:
                df["result"] = df["a"] + df["b"]
            elif operation_type == Operation.soustraction:
                df["result"] = df["a"] - df["b"]
            elif operation_type == Operation.multiplication:
                df["result"] = df["a"] * df["b"]
        elif operation_type == Operation.division:
            a = (np.linspace(1, 12, 12, dtype=int).reshape((12, 1)) * np.ones(12)).flatten()
            b = (np.ones((12, 1)) * np.linspace(1, 12, 12)).flatten()
            result = a * b
            df = pd.DataFrame({"a": result, "b": a, "result": b}, dtype=int)
        else:
            raise NotImplementedError(f"operation_type {operation_type} not defined")
        df = df.query("result >= 0").copy(deep=True)
        df["op"] = operation_type.value
        df["success"] = 0
        df["failure"] = 0
        df["weights"] = 1.0
        df.to_parquet(file_name)


    def create_mask(self, min_b: int, max_b: int):
        self.df["mask"] = 1.0
        self.df.loc[self.df["b"] < min_b, "mask"] = 0.0
        self.df.loc[self.df["b"] > max_b, "mask"] = 0.0


    def sample_rows(self, nb_samples: int):
        df = self.df.assign(weights_mask=self.df["weights"]*self.df["mask"])
        self.df_sampled = df.sample(
            n=nb_samples,
            replace=False,
            weights="weights_mask",
            axis=0
        )
