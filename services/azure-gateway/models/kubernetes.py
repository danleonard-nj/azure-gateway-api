from framework.utilities.pinq import any


class Request:
    def validate(self):
        pass


class KuberenetesLogRequest(Request):
    def __init__(self, namespace, pod, params):
        self.tail = params.get('tail')

        self.namespace = namespace
        self.pod = pod

    def validate(self):
        return not any(items=[
            self.namespace,
            self.pod],
            func=lambda x: x is None)
