import pytest
from cpqa.mut import MutClient
from cpqa.mut.request import MutRequest
from cpqa.mut.request import MultiMutRequest
from cpqa.mut.mut_result import MutResult


def get_mut_client(mocker):
    mock_settings = mocker.patch('cpqa.mut.mut_client.Settings.get', return_value=0x1234)
    return MutClient(True)

def test_open(mocker):
    mut_client = get_mut_client(mocker)
    with pytest.raises(ValueError):
        mut_client.open(-1)

    assert mut_client.open(0) == True
    assert mut_client.open(1) == True
    mock_mut_mock = mocker.patch('cpqa.mut.__mut_mock.MutMock.open', return_value=MutResult(100, "NG", False))
    assert mut_client.open(0) == False

def test_close(mocker):
    mut_client = get_mut_client(mocker)
    mut_client.close()
    mock_mut_mock = mocker.patch('cpqa.mut.__mut_mock.MutMock.close', return_value=MutResult(100, "NG", False))
    mut_client.close()

def test_request(mocker):
    class TestMutRequest(MutRequest):
        @property
        def name(self):
            return "TestMutRequest"

        @property
        def name_short(self):
            return "TestMut"

        @property
        def request_id(self):
            return 0x100

        @property
        def unit(self):
            return "@"

        @property
        def max(self):
            return 100

        @property
        def min(self):
            return 0

        def convert(self, x):
            return x

    class TestMultiMutRequest(MutRequest, MultiMutRequest):

        def __init__(self):
            MutRequest.__init__(self)
            MultiMutRequest.__init__(self)
            self.__sub_requests = [TestMutRequest(), TestMutRequest()]

        @property
        def name(self):
            return "TestMultiMutRequest"

        @property
        def name_short(self):
            return "TestMultiMut"

        @property
        def request_id(self):
            return 0x150

        @property
        def unit(self):
            return "*"

        @property
        def max(self):
            return 100

        @property
        def min(self):
            return 0

        @property
        def sub_requests(self):
            return self.__sub_requests

        def convert(self, x):
            return x

    mut_client = get_mut_client(mocker)
    
    mock_mut_mock = mocker.patch('cpqa.mut.__mut_mock.MutMock.request', return_value=MutResult(100, MutResult.STATUS_OK, True))
    assert mut_client.request(TestMutRequest()) == MutResult(100, MutResult.STATUS_OK, True).value
    assert mut_client.request(TestMultiMutRequest()) == MutResult(100, MutResult.STATUS_OK, True).value

    mock_mut_mock.return_value=MutResult(0, "NG", False)
    assert mut_client.request(TestMutRequest()) == "NG"

    mocker.patch.object(mut_client, "_MutClient__check_connection", return_value=False)
    mock_mut_mock.return_value=MutResult(0, MutResult.STATUS_OK, True)
    assert mut_client.request(TestMutRequest()) is None

def test_exist_device(mocker):
    mut_client = get_mut_client(mocker)
    assert mut_client.exist_device() == True

    
