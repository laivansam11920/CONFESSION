from app.core.exceptions.confession import ConfessionNotFoundException
import uuid


def test_confession_not_found():
    raise ConfessionNotFoundException()


def test_confession_not_found_2():
    raise ConfessionNotFoundException(cfs_id=uuid.uuid4())


try:
    test_confession_not_found_2()
except ConfessionNotFoundException as e:
    res = e.to_response()

    print(res.msg, res.success, res.details, res.error_code, res.status_code)
    print(e.message, e.error_code, e.status_code, e.payload)
