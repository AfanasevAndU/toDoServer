from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator

cluster = Cluster('couchbase://localhost', ClusterOptions(PasswordAuthenticator('Andrusha', 'guffqwbnjopbm45r89))')))
bucket = cluster.bucket('ToDo_backet')
collection = bucket.default_collection()

def get_collection():
    return collection

def get_cluster():
    return cluster
