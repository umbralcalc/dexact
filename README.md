# dexAct

This Python package provides the necessary tools to interact with [dexetera](https://github.com/umbralcalc/dexetera). The two key imports are the `ActionTaker` protocol and the `launch_websocket_server` function.

## Overview

dexAct enables Python code to interact with a dexetera simulation via WebSocket. The simulation sends partitioned state data, and your Python code responds with actions to take.

## How It Works

- A WebSocket server is launched on `ws://localhost:2112`
- The simulation sends `PartitionState` messages containing:
  - `cumulative_timesteps`: the current simulation time
  - `partition_name`: the name of the partition (used as a key)
  - `state`: a list of float values for that partition
- When all expected partitions are received (based on the number of partition keys), your `take_next_action` method is called
- Your method returns a list of floats representing the action to take
- The action is sent back to the simulation via WebSocket

## Usage

Create a class that implements the `ActionTaker` protocol:

```python
from dexact.server import ActionTaker, launch_websocket_server

class ExampleActionTaker(ActionTaker):
    def take_next_action(
        self, 
        time: float, 
        states: dict[str, list[float]]
    ) -> list[float]:
        """
        Args:
            time: The current simulation time (cumulative timesteps)
            states: Dictionary mapping partition names to their state values
        
        Returns:
            A list of floats representing the action to take
        """
        # Example: extract and use some state values
        some_partition_state = states.get("some_partition", [])
        
        # Your control logic here
        action = [1.0, 2.0, 3.0]  # Example action
        
        return action

if __name__ == "__main__":
    # Launch the server and wait for the expected number of partition states
    # In this example, we expect 3 partition states before calling take_next_action
    launch_websocket_server(ExampleActionTaker(), num_state_keys=3)
```
