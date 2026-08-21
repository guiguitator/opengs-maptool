from unittest.mock import MagicMock
import pytest

from opengs_maptool.controllers.progress_controller import (
    ProgressController,
    TaskCancelledInterrupt,
)
import time
from unittest.mock import patch


def test_add_phase_validation_and_add_after_start():
    controller = ProgressController()
    # invalid weights
    for bad in (0, -1, 3.5, "5"):
        with pytest.raises(ValueError):
            controller.add_phase(step_weight=bad)

    # valid add and cannot add after execution started
    p1 = controller.add_phase(step_weight=5, msg="p1")
    with controller.execute_phase(p1):
        with pytest.raises(RuntimeError):
            controller.add_phase(step_weight=2)


def test_track_iteration_type_and_retire_behavior():
    controller = ProgressController()
    # Non-sized iterable should raise
    gen = (i for i in range(3))
    with pytest.raises(TypeError):
        list(controller.track_iteration(gen))


def test_update_progress_validations():
    controller = ProgressController()
    p = controller.add_phase(step_weight=5)

    # Cannot update before started: calling _update_progress should raise because total_steps==0
    with pytest.raises(RuntimeError):
        controller._update_progress(1)

    with controller.execute_phase(p):
        # valid increases
        inc = controller._update_progress(2)
        assert inc == 2

        # decreasing completed steps should raise
        with pytest.raises(ValueError):
            controller._update_progress(1)

        # exceeding total_steps should raise
        with pytest.raises(RuntimeError):
            controller._update_progress(100)


def test_cancel_and_is_cancelled_retire_signal():
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    assert not controller.is_cancelled()
    controller.cancel()
    assert controller.is_cancelled()
    retired.assert_called_once()


def test_execute_phase_early_return_and_retire():
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    p1 = controller.add_phase(step_weight=5, msg="p1")
    p2 = controller.add_phase(step_weight=5, msg="p2")

    def helper():
        with controller.execute_phase(p1):
            return "early"

    # return from inside the with-block completes the phase normally
    helper()

    # Since p1 is not the final phase, it should be advanced to its target
    # but not retire the whole controller.
    retired.assert_not_called()
    assert controller.get_progress_status().completed_steps == p1._target_completed_steps


def test_track_iteration_break_behavior():
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    items = [1, 2, 3, 4]
    seen = []
    for item in controller.track_iteration(items):
        seen.append(item)
        if item == 2:
            break

    assert seen == [1, 2]
    # Only fully completed updates are counted (increment happens after control returns),
    # so breaking on the 2nd item leaves completed_steps at 1.
    assert controller.get_progress_status().completed_steps == 1
    retired.assert_called()


def test_subprogress_with_track_iteration_and_exception_does_not_finish_parent_phase():
    parent = ProgressController()
    retired = MagicMock()
    parent.task_retired.connect(retired)

    parent_phase = parent.add_phase(step_weight=100, msg="parent")

    with pytest.raises(RuntimeError):
        with parent.execute_phase(parent_phase) as sub:
            # Use track_iteration directly on the sub-controller (no configured sub-phases)
            for item in sub.track_iteration([1, 2, 3, 4]):
                if item == 2:
                    raise RuntimeError("boom")

    parent_steps = parent.get_progress_status().completed_steps
    assert parent_steps > 0
    assert parent_steps < parent_phase._target_completed_steps
    retired.assert_called()


def test_cancel_causes_update_to_raise_TaskCancelledInterrupt():
    controller = ProgressController()
    p = controller.add_phase(step_weight=5)
    # Cancellation in the body will cause the context manager to raise
    # a TaskCancelledInterrupt on exit when it attempts the final update.
    with pytest.raises(TaskCancelledInterrupt):
        with controller.execute_phase(p):
            controller.cancel()


def test_sub_cancel_delegates_to_parent():
    parent = ProgressController()
    parent_phase = parent.add_phase(step_weight=5)
    with pytest.raises(TaskCancelledInterrupt):
        with parent.execute_phase(parent_phase) as sub:
            sub.cancel()
            assert parent.is_cancelled()


def test_subprogress_scaling_and_rounding():
    parent = ProgressController()
    parent_phase = parent.add_phase(step_weight=50, msg="parent")

    with parent.execute_phase(parent_phase) as sub:
        # create a sub-phase with 7 steps to exercise rounding behavior
        sub_phase = sub.add_phase(step_weight=7, msg="sub")
        with sub.execute_phase(sub_phase):
            # initial parent completed
            before = parent.get_progress_status().completed_steps

            # advance sub by 1 of 7
            sub._update_progress(1)
            # compute expected parent absolute target using values from sub
            start_offset = sub._parent_start_offset
            budget = sub._step_budget_in_parent
            expected = start_offset + int((1 / sub._status.total_steps) * budget)
            assert parent.get_progress_status().completed_steps == expected

            # advance sub to 4 of 7
            sub._update_progress(4)
            expected2 = start_offset + int((4 / sub._status.total_steps) * budget)
            assert parent.get_progress_status().completed_steps == expected2


def test_track_iteration_continue_behavior_completes():
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    items = [1, 2, 3]
    seen = []
    for item in controller.track_iteration(items):
        seen.append(item)
        if item == 2:
            continue

    assert seen == [1, 2, 3]
    assert controller.get_progress_status().completed_steps == len(items)
    retired.assert_called()


def test_phase_timing_and_durations_recorded():
    controller = ProgressController()
    p = controller.add_phase(step_weight=2, msg="timed")
    with controller.execute_phase(p):
        time.sleep(0.01)

    # duration should be recorded and greater than zero
    assert p in controller._phase_durations
    assert controller._phase_durations[p] >= 0.0


def test_logging_send_called_on_operations(monkeypatch):
    # Patch the logging sender to observe calls
    from opengs_maptool.services import logging_service

    send_mock = MagicMock()
    monkeypatch.setattr(logging_service.LOGGING_SERVICE.loggers.task_progress, 'send', send_mock)

    controller = ProgressController(name="logger-test")
    # execute_as_only_phase must be used on a controller with no configured phases
    with controller.execute_as_only_phase():
        pass

    assert send_mock.called

