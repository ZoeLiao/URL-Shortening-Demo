from django.http import JsonResponse


class CustomJsonResponse(JsonResponse):
    """CustomJsonResponse

    An HTTP response class that inherits JsonResponse
    :param res: A named_tuple imported from backend.results
                and passed to pay_load.
    :param data: A dictionary of kwargs passed to pay_load.

    """
    def __init__(self, res='', data={}, **kwargs):

        self.data = self.set_payload(res, data)

        super(CustomJsonResponse, self).__init__(
            data=self.data,
            **kwargs
        )

    def set_payload(self, res='', data={}):
        payload = {
            'result_code': res.code,
            'result_message': res.msg,
        }
        if res.detail:
            payload['result_detail'] = str(res.detail)
        payload['data'] = data
        return payload
