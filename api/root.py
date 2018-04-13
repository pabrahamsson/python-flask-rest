class Root:
    def get(self) -> dict:
        return 'Redirecting', 301, {'Location': '/v1/ui/'}


class_instance = Root()
