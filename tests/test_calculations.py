import pytest
from app.routers.blog import add

@pytest.mark.parametrize("num1, num2, expected", [
    (1,2,3),
    (2,3,5),
    (5,4,9)
])
def test_add(num1, num2, expected):
    print('testing add function')
    assert add(num1, num2) == expected


