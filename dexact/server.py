import asyncio
import websockets

from typing import Protocol
from websockets.server import WebSocketServerProtocol
from .partition_state_pb2 import PartitionState, State


class ActionTaker(Protocol):
    """
    The Protocol which must be implemented in order to interact
    with a dexetera simulation via websocket.

    The simulation sends partitioned state messages via WebSocket.
    When all partitions are received, take_next_action is called
    with the accumulated states, and the returned action is sent back
    to the simulation.
    """

    def take_next_action(
        self, time: float, states: dict[str, list[float]]
    ) -> list[float]:
        """
        Called when all partition states have been received from the simulation.

        Args:
            time: The current simulation time (cumulative timesteps).
            states: Dictionary mapping partition names to their state values.
                The keys are partition names sent by the simulation,
                and values are lists of floats representing that partition's state.

        Returns:
            A list of floats representing the action to take in the simulation.
        """
        ...


async def _launch_websocket_server(action_taker: ActionTaker, num_state_keys: int):
    """
    Internal async function that sets up and runs the WebSocket server.

    Args:
        action_taker: An instance implementing the ActionTaker protocol.
        num_state_keys: The number of partition states to expect before calling
            take_next_action.
    """
    received_messages: dict[str, list[float]] = {}

    async def _handle(websocket: WebSocketServerProtocol):
        async for binary_message in websocket:
            message = PartitionState()
            message.ParseFromString(binary_message)
            received_messages[message.partition_name] = message.state.values
            if len(received_messages) == num_state_keys:
                action_state = action_taker.take_next_action(
                    message.cumulative_timesteps,
                    received_messages,
                )
                await websocket.send(State(values=action_state).SerializeToString())
                received_messages.clear()

    async with websockets.serve(_handle, "localhost", 2112):
        print("WebSocket server started on ws://localhost:2112")
        await asyncio.Future()


def launch_websocket_server(action_taker: ActionTaker, num_state_keys: int = 1):
    """
    Launch a WebSocket server on ws://localhost:2112 to interact with a dexetera simulation.

    Args:
        action_taker: An instance implementing the ActionTaker protocol.
        num_state_keys: The number of partition states to expect before calling
            take_next_action. Defaults to 1.
    """

    asyncio.run(_launch_websocket_server(action_taker, num_state_keys))
