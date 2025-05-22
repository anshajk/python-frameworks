from openai import OpenAI

client = OpenAI()


class VectorStoreManager:
    def __init__(self):
        self.client = OpenAI()

    def get_all(self):
        vector_stores = self.client.vector_stores.list()
        return vector_stores

    def create(self, name, file_ids):
        response = self.client.vector_stores.create(name=name, file_ids=file_ids)
        return response

    def search_store(self, store_id, query):
        response = self.client.vector_stores.search(
            vector_store_id=store_id, query=query
        )
        return response


if __name__ == "__main__":
    vector_store_manager = VectorStoreManager()
    vector_stores = vector_store_manager.get_all()
    # new_store = vector_store_manager.create(
    #     name="container_info_store", file_ids=["file-R75U5aXXgdKb2cFQZkhPhV"]
    # )
    print(vector_stores)
    result = vector_store_manager.search_store(
        store_id="vs_682f2546d790819181036979dc318aea",
        query="What is the purpose of a Dockerfile? How can I create multiple containers and orchestrate them?",
    )
    print(result)
