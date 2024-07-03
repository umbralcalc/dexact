# DexAct

This Python provides the necessary tools to interact with [dexetera](https://github.com/umbralcalc/dexetera). The two key imports are the `ActionTaker` protocol and the `launch_websocket_server` function. You can use these to create a simple script like this:

```python
from dexact.server import ActionTaker, launch_websocket_server

class ExampleActionTaker(ActionTaker):
    @property
    def state_map(self) -> dict[int, str]:
        return {
            0: "actions",
            1: "another_state",
            ...
        }

    def take_next_action(
        self, 
        time: float, 
        states: dict[str, list[float]]
    ) -> list[float]:
        ...

if __name__ == "__main__":
    launch_websocket_server(ExampleActionTaker())
```
