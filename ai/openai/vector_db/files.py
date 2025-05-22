from openai import OpenAI
import os


class FileStore:
    def __init__(self):
        self.client = OpenAI()

    def get_all(self):
        file_stores = self.client.files.list()
        return file_stores
    def upload(self, file_path):
        with open(file_path, "rb") as file:
            response = self.client.files.create(file=file, purpose='user_data')
        return response
    

if __name__ == "__main__":
    file_store = FileStore()
    file_stores = file_store.get_all()
    print(file_stores)
    # Example of uploading a file
    # file_path = os.path.join(os.path.dirname(__file__), "CICD_with_Docker_Kubernetes_Semaphore.pdf")
    # response = file_store.upload(file_path)
    # print(response)