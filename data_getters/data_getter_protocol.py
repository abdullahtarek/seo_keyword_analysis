from typing import Protocol,List
from pandas import DataFrame

class DataGetterProtocol(Protocol):
    def get_data(self, keywords: List[str]) -> DataFrame:
        """Add your code to fetch data based on keywords and create a dataframe
        The DataFrame should have at least two columns. 
        The first column should be named 'Keyword' and should contain the keywords. 
        And the other column contains enriching data about this keyword"""