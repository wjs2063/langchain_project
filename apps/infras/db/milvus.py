from pymilvus import DataType, MilvusClient

client = MilvusClient(
    uri="http://127.0.0.1:19530",
)

# res = client.describe_index(collection_name="incar_example_LX3")
#
# print(res)
