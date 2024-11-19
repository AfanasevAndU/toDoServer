from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import Collection

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('Andrusha', 'guffqwbnjopbm45r89))')))
bucket = cluster.bucket('ToDo_backet') 
collection = bucket.default_collection()

def get_collection():
    return collection

def get_cluster():
    cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('Andrusha', 'guffqwbnjopbm45r89))')))
    return cluster