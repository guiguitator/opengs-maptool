# Tutorial: Write background tasks with live progress bars
> This document is intended for developers. It is not relevant for users of the app.
#### Author: @GermanCodeEngineer, 19. August 2026

This tutorial uses the class [`ProgressController`](../../opengs_maptool/controllers/progress_controller.py).

## Basic convention
A background function running in a background thread or process should recieve a fresh `ProgressController` instance, next to it's other parameters. [`TaskController`](../../opengs_maptool/controllers/task_controller.py) automatically handles the creation of this instance for top-level task functions.
- Note: the parameter must be a keyword argument called `progress_controller` if it's called by the `TaskController`.
```py
def function_for_my_task(my_param: int, progress_controller: ProgressController):
    ...
```

## Configuring phases
As the UI must know which phases exist and their relative size, the task function should configure it's phases before executing anything:
```py
def function_for_my_task(my_param: int, progress_controller: ProgressController):
    # Returns a phase reference object
    phase1 = progress_controller.add_phase(step_weight=500)
    phase2 = progress_controller.add_phase(step_weight=1000, msg="Doing Phase 2")
    phase3 = progress_controller.add_phase(step_weight=300)

    ...
```
> Ideally, you should use high step weights. You can read the app logs to measure how long each phase roughly takes to execute, when you are done writing your task. You should then **proportionally assign your step weights.**

## Executing actual task code
All of the actual task should be wrapped in `with`-clauses using execution methods. This provides many benefits like automatic updates for the UI on errors or safe usage of early `return`, `break` or `continue`.
Always be aware of this: The user can cancel a task in the UI or try to close the app: In this case, the `TaskController` waits until the next phase is completed or a `track_iteration` iteration is completed and then stops the task using a `TaskCancelledInterrupt` (subclass of `BaseException`). However if the task still hasn't reached a breakpoint after a few seconds, the user can forcefully stop the task.

### Executing a simple phase
```py
def function_for_my_task(progress_controller: ProgressController):
    # Returns a phase reference object
    phase1 = progress_controller.add_phase(step_weight=500)
    phase2 = progress_controller.add_phase(step_weight=1000, msg="Doing Phase 2")
    phase3 = progress_controller.add_phase(step_weight=300)

    with progress_controller.execute_phase(phase1): # use the reference object
        ... # Do phase 1 logic here

    ...
```

### Executing a complex phase
If you want to call a function in your task (which accepts a `ProgressController` too) or do multiple time-consuming things, you can use a `SubProgressController` to create further sub-phases or fresh controllers to pass to a function.
```py
...
# Get a sub-progress controller, that can be configured with sub-phases.
# Best practice: leave sub-phase configuration in control of the subfunction
# It automatically updates progress in parent controller in a scaled manner.
with progress_controller.execute_phase(phase2) as sub_progress_phase2:
    x = function_for_phase2(sub_progress_phase2)
...
```
OR:
```py
...
with progress_controller.execute_phase(phase2) as sub_progress_phase2:
    # We can't just give sub_progress_phase2 to the sub-function as we also need other phases, so create sub-phases.
    phase2_a = sub_progress_phase2.add_phase(step_weight=300) # Again carefully pick weights
    phase2_b = sub_progress_phase2.add_phase(step_weight=45)

    with sub_progress_phase2.execute_phase(phase2_a):
        if my_condition:
            return 345

        x = y + z

    with sub_progress_phase2.execute_phase(phase2_b) as sub_progress_phase2_b:
        x = another_function(sub_progress_phase2_b, y=y)

    if x > 0:
        return x
...
```

### Executing loops
For-Loops are a special case. Use `progress_controller.track_iteration` to track the iteration of a **sized iterable**.
```py
def function_for_iterable_task(progress_controller: ProgressController, items: Iterable):
    for item in progress_controller.track_iteration(items):
        ... # process item
    # WARNING: Now `progress_controller` of this function is consumed and can not be reused.
```

### Single phase shortcut
There is a shortcut when e.g. your sub-function used in a task has only one phase or can't really be split into phases:
```py
def function_for_simple_task(progress_controller: ProgressController):
    with progress_controller.execute_as_only_phase() as ctrl:
        ... # Do phase 1
    # Now `progress_controller` of this function is consumed and can not be reused.
```

> You can see a real usage example in [`opengs_maptool/logic/territory_generator.py`](../../opengs_maptool/logic/territory_generator.py).
