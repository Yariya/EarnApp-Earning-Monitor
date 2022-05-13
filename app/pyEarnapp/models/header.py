
class Headers:
    def __init__(self, auth_refresh_token) -> None:
        self.params = (
            ('appid', 'earnapp_dashboard'),
        )
        self.header = {
            'cookie': f'xsrf-token=JzpAP0rchWbX-0dQvhEk0SZv;auth=1; auth-method=google; oauth-refresh-token={auth_refresh_token}',
            'xsrf-token': 'JzpAP0rchWbX-0dQvhEk0SZv',
        }
