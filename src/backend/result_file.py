import logging
from pathlib import Path

import pandas as pd

from src.utils.constants import file_path, map_sym_text_op

logger = logging.getLogger(__name__)
COLS = [
    "a",
    "op",
    "b",
    "answers",
    "result",
    "success",
    "failure",
    "session_datetime",
    "weights",
    "mask",
    "weights_mask",
    "total_time_spent",
    "time_spent_per_op",
]


class ResultFile:
    def __init__(
        self,
        user_name: str,
        result_table: pd.DataFrame,
        total_time_spent: float,
    ):
        self.user_name = user_name
        self.result_table = result_table
        self.total_time_spent = total_time_spent
        self.log_file = None
        self._process_result_file()

    def _process_result_file(self):
        # add timestamp
        if "answers" not in self.result_table.columns:
            logger.error(
                f"Could not find column 'answer' in input Dataframe. "
                + f"Only found: {self.result_table.columns}"
            )
            raise ValueError
        self.result_table["session_datetime"] = pd.Timestamp.utcnow().tz_convert(
            "US/Eastern"
        )
        # Extract operation
        op = self.result_table["op"].unique().item()
        self.operation_type = map_sym_text_op[op]
        logger.debug(f"self.operation_type={self.operation_type}")
        # success / failure
        self.result_table["success"] = 0
        self.result_table.loc[
            self.result_table["answers"] == self.result_table["result"], "success"
        ] = 1
        self.nb_correct = self.result_table["success"].sum()
        self.result_table["failure"] = 0
        self.result_table.loc[
            self.result_table["answers"] != self.result_table["result"], "failure"
        ] = 1
        self.nb_failure = self.result_table["failure"].sum()
        # Process time
        self.result_table["total_time_spent"] = self.total_time_spent
        self.result_table["time_spent_per_op"] = self.total_time_spent / len(
            self.result_table
        )
        # Check result_file
        check_COLS = all([col in self.result_table.columns for col in COLS])
        if not check_COLS:
            logger.error(f"self.result_file.columns={self.result_table.columns}")
            raise ValueError

    @property
    def log_filename(self) -> Path:
        return Path(
            file_path, f"log_{self.user_name}_{self.operation_type.name}.parquet"
        )

    def analyze_results(self) -> str:
        total_len = len(self.result_table)
        time_per_op = self.result_table["time_spent_per_op"].unique().item()
        output_text = "Bravo, tu as terminé. Place aux résultats!\n"
        output_text += f"Tu as passé {time_per_op:.1f} secondes par question.\n"
        output_text += (
            f"Sur les {total_len} questions demandées, "
            + f"tu as eu {self.nb_correct} bonnes réponses (BRAVO!!), et tu as eu {self.nb_failure} erreur(s).\n"
        )
        if self.nb_failure > 0:
            output_text += "Voici les questions que tu as besoin de travailler:\n"
            df_tmp = self.result_table.query("failure==1")
            output_text += (
                df_tmp["a"].astype(str)
                + " "
                + df_tmp["op"]
                + " "
                + df_tmp["b"].astype(str)
                + " = "
                + df_tmp["result"].astype(str)
                + " (ta réponse: "
                + df_tmp["answers"].astype(str)
                + ")"
            ).to_string(index=False)
        return output_text

    def update_logfile(self):
        self._load_log_file()
        self.log_file = pd.concat(
            [self.log_file[COLS], self.result_table[COLS]], axis=0
        )
        self._save_log_file()

    def _load_log_file(self):
        if not self.log_filename.exists():
            logger.warning(
                f"Could not find {self.log_filename}. " + "Creating an empty DataFrame."
            )
            self.log_file = pd.DataFrame(columns=COLS)
        else:
            logger.info(f"Loading {self.log_filename}")
            self.log_file = pd.read_parquet(self.log_filename)

    def _save_log_file(self):
        logger.info(f"Writing self.log_file to {self.log_filename}")
        self.log_file.to_parquet(self.log_filename)

    def calculate_score(self) -> pd.DataFrame:
        if self.log_file is None:
            return pd.DataFrame()
        df_sums = self.log_file.groupby("session_datetime")[["success", "failure"]].sum()
        df_sums["total"] = df_sums["success"] + df_sums["failure"]
        df_sums["pct_success"] = df_sums["success"] / df_sums["total"]

        df_last = self.log_file.groupby("session_datetime")["time_spent_per_op"].last().to_frame()
        
        df_res = df_last.join(df_sums[["pct_success"]], how="left")
        df_res["score"] = 100.0 * df_res["pct_success"] / df_res["time_spent_per_op"]
        df_res["index"] = range(1, len(df_res)+1)
        return df_res.sort_index(ascending=True)