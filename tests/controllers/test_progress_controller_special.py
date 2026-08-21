from unittest.mock import MagicMock
import pytest

from opengs_maptool.controllers.progress_controller import ProgressController
from opengs_maptool.models.progress_status import ProgressStatus


def test_add_phase_and_task_started_signal_emitted():
    controller = ProgressController()
    started = MagicMock()
    controller.task_started.connect(started)

    # Configure phases
    p1 = controller.add_phase(step_weight=5, msg="Phase 1")
    p2 = controller.add_phase(step_weight=10, msg="Phase 2")

    # Enter first phase - should emit task_started and phase_started
    phase_started = MagicMock()
    controller.task_phase_started.connect(phase_started)

    with controller.execute_phase(p1) as sub:
        # Task was started and phase was announced
        started.assert_called_once()
        phase_started.assert_called_once()
        status: ProgressStatus = started.call_args[0][0]
        assert status.total_steps == 15
        assert status.completed_steps == 0


def test_execute_as_only_phase_completes_and_emits_update_and_retire():
    controller = ProgressController()
    updated = MagicMock()
    retired = MagicMock()
    controller.task_progress_updated.connect(updated)
    controller.task_retired.connect(retired)

    with controller.execute_as_only_phase():
        # inside block nothing done; on exit the single step should be applied
        pass

    # One update on exit (0 -> 1) and then retired
    assert updated.call_count == 1
    updated_status, delta = updated.call_args[0]
    assert updated_status.completed_steps == 1
    assert delta == 1
    retired.assert_called_once()


def test_execute_as_only_phase_handles_exceptions_and_does_not_mark_finished():
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    with pytest.raises(RuntimeError):
        with controller.execute_as_only_phase():
            raise RuntimeError("fail")

    # Retired should have been called but completed_steps must not be set to 1
    retired.assert_called_once()
    assert controller.get_progress_status().completed_steps == 0


def test_track_iteration_completes_normally_and_on_error():
    # Normal completion
    controller = ProgressController()
    retired = MagicMock()
    controller.task_retired.connect(retired)

    items = [1, 2, 3]
    seen = []
    for item in controller.track_iteration(items):
        seen.append(item)

    assert seen == items
    assert controller.get_progress_status().completed_steps == 3
    retired.assert_called()

    # Error case: ensure exception propagates and progress is not set to total
    controller2 = ProgressController()
    retired2 = MagicMock()
    controller2.task_retired.connect(retired2)

    items2 = [1, 2, 3]
    seen2 = []
    with pytest.raises(RuntimeError):
        for item in controller2.track_iteration(items2):
            seen2.append(item)
            if item == 2:
                raise RuntimeError("boom")

    # Only items up to the error were processed (generator did yield the second
    # item, but the generator's internal completed counter only increments
    # after control returns to it; therefore completed_steps reflects the last
    # *fully* completed update)
    assert seen2 == [1, 2]
    # Progress should reflect only the fully applied updates (1 in this case)
    assert controller2.get_progress_status().completed_steps == 1
    retired2.assert_called()


def test_sub_progress_propagation_and_no_final_target_on_exception():
    parent = ProgressController()
    # Parent phase of weight 50
    parent_phase = parent.add_phase(step_weight=50, msg="parent")

    with pytest.raises(RuntimeError):
        with parent.execute_phase(parent_phase) as sub:
            # configure sub with 10 steps
            sub_phase = sub.add_phase(step_weight=10, msg="sub")
            with sub.execute_phase(sub_phase):
                # advance sub by 2 steps -> should propagate to parent
                sub._update_progress(2)
                # Now raise to abort the phase
                raise RuntimeError("subfail")

    # Parent should have been advanced by a scaled amount, but NOT set to the parent's phase target (50)
    parent_steps = parent.get_progress_status().completed_steps
    assert parent_steps > 0
    assert parent_steps < parent_phase._target_completed_steps
