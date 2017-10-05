import io
import json

import pytest
import requests

import htttea


def test_response():
    body = b"Hello World"
    with htttea.Htttea() as t3:
        t3.response = htttea.Response(body=body)
        assert requests.get(t3.url).text == body.decode()


def test_wait_until_request_no_request():
    with htttea.Htttea() as t3:
        with pytest.raises(htttea.TimeoutError):
            t3.wait_until_request(timeout=0.0001)


def test_wait_until_request():
    with htttea.Htttea() as t3:
        requests.get(t3.url)
        try:
            t3.wait_until_request(timeout=0.0001)
        except htttea.TimeoutError:
            pytest.fail()


class TestPost:
    def test_form_data(self):
        data = {
            'Hello': "World"
        }
        with htttea.Htttea() as t3:
            requests.post(t3.url, data=data)
            assert t3.request.data == data

    def test_form_upload(self):
        file_content = b"I'm a file."
        data = {
            'Hello': "World"
        }
        with htttea.Htttea() as t3:
            requests.post(t3.url, data=data, files={'file': io.BytesIO(file_content)})
            assert t3.request.data['file'] == file_content
            assert t3.request.data['Hello'] == "World"

    def test_json(self):
        data = {
            'Hello': "World"
        }
        with htttea.Htttea() as t3:
            requests.post(t3.url, json=data)
            assert json.loads(t3.request.raw_body.decode()) == data
