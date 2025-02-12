from langflow.custom import Component
from langflow.io import Output
from langflow.schema import Data
import logging
import cassio
from langflow.io import SecretStrInput, StrInput

class AstraDBCQL(Component):
    logger = logging.getLogger(__name__)
    display_name = "AstraDBCQL"
    description = "Make CQL queries to AstraDB."
    documentation: str = "https://docs.datastax.com/en/astra-db-serverless/cql/develop-with-cql.html"
    name = "AstraDB"
    icon: str = "AstraDB"

    inputs = [
        SecretStrInput(name="token", display_name="Astra DB Application Token", info="Authentication token for accessing Astra DB.", value="ASTRA_DB_APPLICATION_TOKEN", required=True),
        SecretStrInput(name="database_id", display_name="Database", info="The Astra DB Database to use.",required=True, ),  
        StrInput(name="keyspace", display_name="keyspace", info="keyspace name", value="demo"),      
        StrInput(name="query", display_name="query", info="Query to execute", tool_mode=True,),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="search_documents"),
    ]

    def search_documents(self) -> list[Data]:
        cassio.init(token=self.token, database_id=self.database_id)
        session = cassio.config.resolve_session()        
        if not session:
            raise Exception(
                "Check environment configuration or manually configure cassio connection parameters"
                )
        session.set_keyspace(keyspace=self.keyspace)        
        docs = session.execute(self.query).all()
        documents = []
        for row in docs:
            row_dict = dict(row._asdict())
            metadata = {key: value for key, value in row_dict.items()}                
            documents.append(Data(data=metadata))            
        self.status = documents
        return documents