from locust import HttpUser, task


class LocustTestUser(HttpUser):
    @task
    def get_test(self):
        self.client.get("/test")
