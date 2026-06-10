class HealthMockRepository:
    def __init__(self):
        pass

    async def select_one(self,schema_name:str, table_name:str ):
        return {"schema_name": schema_name, "table_name": table_name}
        