import random
from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)  # Time between requests in seconds

    def on_start(self):
        # Define user credentials
        self.user_name = "mubashar"
        self.password = "Mubashar64."
        self.auth = HTTPBasicAuth(self.user_name, self.password)

    @task(10)
    def propfind(self):
        self.client.request("PROPFIND", "/remote.php/webdav", auth=self.auth)

    @task(10)
    def login(self):
        self.client.get("/index.php/login", auth=self.auth)

    @task(5)
    def read_file(self):
        self.client.get("/index.php/apps/files/", auth=self.auth)

    @task(1)
    def upload_file(self):
        # Simulate uploading a file
        file_content = "This is a test file content."
        file_name = f"test_file_{random.randint(1, 100)}.txt"
        self.client.put(f"/remote.php/dav/files/{self.user_name}/{file_name}", data=file_content, auth=self.auth)

    @task(1)
    def logout(self):
        self.client.get("/index.php/logout", auth=self.auth)