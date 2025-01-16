import json
from typing import Dict, Any

from pydantic import BaseModel

# Basic structure of the AIXP message using Pydantic
class AIXPMessage(BaseModel):
    sender_id: str
    receiver_id: str
    task: str
    data: Dict[str, Any]

# Agent A (Requester)
class AgentA:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def request_length(self, receiver_url: str, text: str):
        message = AIXPMessage(
            sender_id=self.agent_id,
            receiver_id="AgentB",
            task="get_length",
            data={"text": text}
        )
        headers = {'Content-type': 'application/json'}
        response = requests.post(receiver_url, data=message.model_dump_json(), headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()

# Agent B (Service Provider)
class AgentB:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def process_request(self, message_json: str) -> str:
        try:
            message = AIXPMessage.model_validate_json(message_json)
            if message.task == "get_length":
                length = len(message.data["text"])
                response = AIXPMessage(
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    task="length_obtained",
                    data={"length": length}
                )
                return response.model_dump_json()
            else:
                return json.dumps({"error": "Task not recognized"})
        except Exception as e:
            return json.dumps({"error": f"Error processing request: {str(e)}"})

# Simple simulation (without a real HTTP server for now)
if __name__ == "__main__":
    agent_a = AgentA("AgentA")
    agent_b = AgentB("AgentB")

    text_to_analyze = "This is a test text."
    # Simulation of sending and receiving (without a real network)
    message_to_send = AIXPMessage(agent_a.agent_id, agent_b.agent_id, "get_length", {"text": text_to_analyze})
    response_b_json = agent_b.process_request(message_to_send.model_dump_json())
    response_b = AIXPMessage.model_validate_json(response_b_json)

    print(f"Agent A sent: {text_to_analyze}")
    print(f"Agent B responded with the length: {response_b.data['length']}")
