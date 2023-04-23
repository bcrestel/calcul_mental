from pathlib import Path
import logging

import numpy as np
import pandas as pd

from src.constants import Operation, file_path, factor_change_in_weights

logger = logging.getLogger(__name__)

class SummaryFile:
    def __init__(self, user_name: str, operation_type: Operation):
        self.user_name = user_name.lower()
        self.operation_type = operation_type
        logger.debug(f"operation_type={self.operation_type}")
        self._load_summary_file()
        self.df_sampled = None

    def _load_summary_file(self):
        if not self.file_name.exists():
            logger.info(f"Could not find {self.file_name}. Creating default one")
            self._create_file(self.operation_type, self.file_name)
        logger.info(f"Loading {self.file_name}")
        self.df = pd.read_parquet(self.file_name)

    def _save_summary_file(self):
        logger.info(f"Writing self.df to {self.file_name}")
        cols = ["a", "b", "result", "op", "success", "failure", "weights"]
        self.df[cols].to_parquet(self.file_name)

    @property
    def file_name(self) -> Path:
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
        df["weights"] = SummaryFile._calculate_weights(
            df_failure=df["failure"],
            df_success=df["success"],
        )
        df.to_parquet(file_name)

    # TODO: do not log that do self.df as this is temporary
    def create_mask(self, min_b: int, max_b: int):
        self.df["mask"] = 1.0
        self.df.loc[self.df["b"] < min_b, "mask"] = 0.0
        self.df.loc[self.df["b"] > max_b, "mask"] = 0.0

    def sample_rows(self, nb_samples: int) -> pd.DataFrame:
        df = self.df.assign(weights_mask=self.df["weights"]*self.df["mask"])
        cols = ["a", "op", "b", "result", "weights", "mask", "weights_mask"]
        return df.sample(
            n=nb_samples,
            replace=False,
            weights="weights_mask",
            axis=0
        )[cols]

    @staticmethod
    def _calculate_weights(df_failure: pd.Series, df_success: pd.Series) -> pd.Series:
        return 1.0 * (factor_change_in_weights ** (df_failure - df_success))

    def _calculate_weights_from_success_failure(self):
        self.df["weights"] = self._calculate_weights(
            df_failure=self.df["failure"],
            df_success=self.df["success"],
        )

    def update_from_answers(self, result_table: pd.DataFrame):
        # update good answers
        idx_good_answers = result_table.query("success==1").index
        self.df.loc[idx_good_answers, "success"] =+ 1
        logger.debug(f"idx_good_answers={idx_good_answers}")
        # update bad answers
        idx_bad_answers = result_table.query("failure==1").index
        self.df.loc[idx_bad_answers, "failure"] =+ 1
        logger.debug(f"idx_bad_answers={idx_bad_answers}")

        assert len(idx_good_answers) + len(idx_bad_answers) == len(result_table)

        self._calculate_weights_from_success_failure()
        logger.debug(f"self.df.loc[summaryfile_session.index]=\n{self.df.loc[result_table.index]}")

        self._save_summary_file()
