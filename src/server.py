import asyncio
import websockets

from typing import Protocol
from websockets.server import WebSocketServerProtocol
from .partition_state_pb2 import PartitionState, State


class ActionTaker(Protocol):
    """
    The Protocol which must be implemented in order interact
    with a dexetera simulation via websocket.
    """

    @property
    def state_map(self) -> dict[int, str]:
        """
        A dictionary which maps incoming simulation state 
        indices into their string names for convenient access.
        """
        ...
    
    def take_next_action(
        self, 
        time: float, 
        states: dict[str, list[float]]
    ) -> list[float]:
        """
        A method which defines the Python code interaction with 
        a dexetera simulation.

        Args:
            time: float
                The current time value of the simulation states.
            states: dict[str, list[float]]
                The current states of the simulation.

        Outputs:
            action: list[float]
                The next action to take in the simulation.
        """
        ...


async def _launch_websocket_server(action_taker: ActionTaker):
    received_messages: dict[int, list[float]] = {}

    async def _handle(websocket: WebSocketServerProtocol, path: str):
        async for binary_message in websocket:
            message = PartitionState()
            message.ParseFromString(binary_message)
            received_messages[
                action_taker.state_map[message.partition_index]
            ] = message.state.values
            if len(received_messages) == len(action_taker.state_map):
                action_state = action_taker.take_next_action(
                    message.cumulative_timesteps, 
                    received_messages,
                )
                await websocket.send(State(values=action_state).SerializeToString())
                received_messages.clear()

    async with websockets.serve(_handle, "localhost", 2112):
        print("WebSocket server started on ws://localhost:2112")
        await asyncio.Future()


def launch_websocket_server(action_taker: ActionTaker):
    """A convenience method to launch a server on ws://localhost:2112."""

    asyncio.run(_launch_websocket_server(action_taker))