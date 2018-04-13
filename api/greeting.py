from prometheus_client import Counter, Histogram

counter = Counter('greeting_counter', 'Number of greetings')
histogram= Histogram('greeting_response_latency_seconds', 'Response latency (seconds)')

class Greeting:
    @histogram.time()
    def get(self, name) -> dict:
        counter.inc()
        message = {
            "id": int(counter._value.get()),
            "content": "Hello, {name}!".format(name=name)
        }
        return message


class_instance = Greeting()
