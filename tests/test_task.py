import zam.task
import datetime
import unittest


class task_empty(zam.task.task):
    def run(self) -> None:
        return None


def test_a(mocker) -> None:
    START_T = datetime.datetime(2021, 12, 4, 14, 47, 35)
    MINUTE = datetime.timedelta(minutes=1)
    time_now = START_T

    task_a = mocker.Mock(name="task_a")
    task_a.get_next_runtime.side_effect = [
        START_T + 1 * MINUTE,
        START_T + 0 * MINUTE,
        START_T + 3 * MINUTE,
        None,
    ]

    task_b = mocker.Mock(name="task_b")
    task_b.get_next_runtime.side_effect = [START_T + 2 * MINUTE, None]

    tasks = [task_a, task_b]

    manager = mocker.Mock()
    for task in tasks:
        manager.attach_mock(task, task._extract_mock_name())

    dt_min = datetime.datetime.min
    with unittest.mock.patch(
        "zam.task.datetime.datetime"
    ) as mock_datetime, unittest.mock.patch(
        "zam.task.time.sleep"
    ) as mock_sleep:
        mock_datetime.utcnow = mocker.Mock(
            name="utcnow getter", side_effect=lambda: time_now
        )
        mock_datetime.min = dt_min

        def fake_sleep(seconds: float):
            nonlocal time_now
            time_now += datetime.timedelta(seconds=seconds)

        mock_sleep.side_effect = fake_sleep

        zam.task.run_tasks(tasks)

    expected_calls = [
        unittest.mock.call.task_a.get_next_runtime(),
        unittest.mock.call.task_b.get_next_runtime(),
        unittest.mock.call.task_a.run(),
        unittest.mock.call.task_a.get_next_runtime(),
        unittest.mock.call.task_a.run(),
        unittest.mock.call.task_a.get_next_runtime(),
        unittest.mock.call.task_b.run(),
        unittest.mock.call.task_b.get_next_runtime(),
        unittest.mock.call.task_a.run(),
        unittest.mock.call.task_a.get_next_runtime(),
    ]
    assert manager.mock_calls == expected_calls
