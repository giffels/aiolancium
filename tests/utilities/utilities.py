import asyncio


def async_return(*args, return_value=None, **kwargs):
    f = asyncio.Future()
    f.set_result(return_value)
    return f


def run_async(coroutine, *args, **kwargs):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    return loop.run_until_complete(coroutine(*args, **kwargs))


def set_awaitable_return_value(mocked_coroutine, return_value):
    # isinstance does not work due to inheritance
    # iswaitable, iscoroutine not because RuntimeWarning (not awaited)
    # comparing type(...) did not solve the problem as well.
    if not mocked_coroutine.__class__.__name__ == "MagicMock":
        mocked_coroutine.return_value = return_value
    else:  # pass test on Python 3.6 and 3.7
        mocked_coroutine.return_value = async_return(return_value=return_value)
