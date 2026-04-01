from abc import ABC, abstractmethod
import pandas as pd
from dataclasses import dataclass
from typing import Optional, Any, Dict, List

@dataclass
class QueryResult:
    sql: str
    status: str
    engine: str
    data: Optional[Any] = None
    metrics: Optional[Dict] = None
    profile: Optional[Any] = None
    error: Optional[str] = None

class QueryRunner(ABC):
    @abstractmethod
    def run_query(self, sql: str) -> QueryResult:
        pass

    @abstractmethod
    def display_metrics(self, result: QueryResult):
        pass
    
    def display_result_head(self, result:QueryResult, model:str="model unknown", prompt_label:str="prompt label unknown", num_rows:int=500):
        print("\n==============================")
        print(f"({model}) {prompt_label}:\n")

        if result is None:
            print("(No result object)")
        else:
            data = result.data
            if data is None:
                print("(No data)")

            elif isinstance(data, pd.DataFrame):
                print(data.head())
            else:
                print(str(data)[:num_rows])
        
        print("==============================\n")

