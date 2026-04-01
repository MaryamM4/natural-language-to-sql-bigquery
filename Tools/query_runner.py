from abc import ABC, abstractmethod
import pandas as pd

class QueryRunner(ABC):
    @abstractmethod
    def run_query(self, sql: str):
        pass

    @abstractmethod
    def display_metrics(self, result):
        pass
    
    def display_result_head(self, result, model=None, prompt_label=None):
        print("\n==============================")
        print(f"({model}) {prompt_label}:\n")

        data = result.get("data")
        if data is None:
            print("(No data)")
        elif isinstance(data, pd.DataFrame):
            print(data.head())
        else:
            print(str(data)[:500])
        
        print("==============================\n")

