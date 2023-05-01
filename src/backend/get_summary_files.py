from typing import Tuple
import logging

import pandas as pd

from src.backend.summary_file import SummaryFile
from src.utils.constants import Operation

logger = logging.getLogger(__name__)


def get_summary_files(
        user_name: str, 
        operation_type: Operation,
        min_b: int,
        max_b: int,
        nb_questions: int,
) -> Tuple[SummaryFile, pd.DataFrame]:
    summaryfile = SummaryFile(user_name=user_name, operation_type=operation_type)
    summaryfile.create_mask(min_b=min_b, max_b=max_b)
    summaryfile_session = summaryfile.sample_rows(nb_samples=nb_questions)
    logger.debug(summaryfile_session)
    logger.debug(summaryfile_session.dtypes)
    logger.debug(summaryfile.df.loc[summaryfile_session.index])
    return summaryfile, summaryfile_session