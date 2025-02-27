# locustfile.py
from locust import HttpUser, task, between
import json

class BreadSalesUser(HttpUser):
    wait_time = between(1, 5)  # 用户在每次请求之间等待1到5秒

    @task
    def test_bread_recommendation(self):
        user_id = 1  # 假设用户ID为1，可根据实际情况修改
        headers = {'Content-Type': 'application/json'}
        response = self.client.get(f'/recommend_bread/{user_id}/', headers=headers)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
        else:
            try:
                data = json.loads(response.text)
                # 可以在这里添加更多的验证逻辑，例如检查返回数据的格式等
            except json.JSONDecodeError:
                print("Failed to decode JSON response")