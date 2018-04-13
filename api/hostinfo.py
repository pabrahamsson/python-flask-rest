from prometheus_client import Counter, Histogram
from socket import gethostname

counter = Counter('hostinfo_counter', 'Number of hostinfo requests')
histogram = Histogram('hostinfo_response_latency_seconds', 'Response latency (seconds)')

class Hostinfo:
    @histogram.time()
    def get(self) -> dict:
        counter.inc()
        message = {
            "id": int(counter._value.get()),
            "hostname": gethostname()
        }
        return message


class_instance = Hostinfo()
