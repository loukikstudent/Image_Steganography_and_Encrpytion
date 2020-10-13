import json
from typing import Dict, Any

from cassandra.cluster import Cluster, EXEC_PROFILE_DEFAULT, ExecutionProfile, ConsistencyLevel
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import dict_factory


class Cassandra_db:
    def __init__(self, keyspace, table):
        self.keyspace = keyspace
        self.table_name = table
        self.profile = ExecutionProfile(load_balancing_policy=WhiteListRoundRobinPolicy(['127.0.0.1']),
                                        retry_policy=DowngradingConsistencyRetryPolicy(),
                                        consistency_level=ConsistencyLevel.QUORUM,
                                        request_timeout=20,
                                        row_factory=dict_factory
                                        )
        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: self.profile})

        # Checking if keyspace exists or not
        # noinspection PyBroadException
        try:
            self.session = self.cluster.connect('d3')
        except Exception as e:
            self.session = self.cluster.connect()
            self.session.execute(
                "CREATE KEYSPACE d3 WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':3} AND durable_writes = 'true';")
            self.session.set_keyspace('d3')

        # checking if the table exists or not
        if self.table_name not in self.cluster.metadata.keyspaces['d3'].tables:
            self.session.execute(
                f"CREATE TABLE {self.table_name} (uuid text , key text , data text , PRIMARY KEY ((uuid,key),data));")

    def __del__(self):
        self.cluster.shutdown()

    def add(self, jsonData: Dict[str, Any]):
        try:
            self.session.execute(
                f"INSERT INTO {self.table_name} (uuid,key,data) VALUES (%(uuid)s,%(key)s,%(data)s) USING TTL 3600;",
                json.loads(jsonData))
            return True
        except Exception as e:
            print("Error while adding")
            print(e)
            return False

    def get(self, query: Dict[str, Any]):
        try:
            return self.session.execute(f"""
                SELECT data FROM {self.table_name}
                WHERE uuid = %(uuid)s and key = %(key)s;
            """, json.loads(query))
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    jsonData = {'uuid': '100', 'key': '12341234', 'data': 'helloWorld!'}
    jsonData = json.dumps(jsonData)

    db = Cassandra_db('d3', 'ikd')
    db.add(jsonData)
    result = db.get(jsonData)
    print(type(result))
    print(result)
    print([i for i in result])
