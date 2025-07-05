import chainlit as cl
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole
import os

project_endpoint = os.environ["PROJECT_ENDPOINT"]
agent_id = os.environ["AGENT_ID"]

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)

def reformat_citations(content_block):
    annotations = content_block.get("annotations", [])
    paragraph = content_block["value"]
    
    # Map citation_title -> set of placeholders
    citation_map = {}
    for annotation in annotations:
        if annotation["type"] == "url_citation":
            placeholder_text = annotation["text"]
            citation_title = annotation["url_citation"]["title"]
            citation_map.setdefault(citation_title, set()).add(placeholder_text)

    # Remove all placeholders from the paragraph
    for placeholders in citation_map.values():
        for placeholder_text in placeholders:
            paragraph = paragraph.replace(placeholder_text, "")

    # If there's at least one citation, append "Source: ..." at the end
    if citation_map:
        sources = ", ".join(citation_map.keys())
        paragraph = paragraph.strip() + f" Source: {sources}"

    return paragraph

@cl.on_chat_start
def on_chat_start():
    # Initialize the user session with the thread ID if it doesn't exist
    if not cl.user_session.get("thread_id"):
        # Create a new thread for the user
        thread = project_client.agents.threads.create()

        # Set the thread ID in the user session
        cl.user_session.set("thread_id", thread.id)
        print(f"New Thread ID: {thread.id}")
              
@cl.on_message
async def main(message: cl.Message):
    
    # Get the thread ID from the user session
    thread_id = cl.user_session.get("thread_id")

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread_id,
        role="user",  # Role of the message sender
        content=message.content,  # Message content
    )
    
     # Create and process agent run in thread with tools
    run = project_client.agents.runs.create_and_process(thread_id=thread_id, agent_id=agent_id)
    print(f"Run finished with status: {run.status}")

    # Check the status of the run and print the result
    if run.status == "failed":
        response = run.last_error
    elif run.status == "completed":
        last_msg = project_client.agents.messages.get_last_message_text_by_role(thread_id=thread_id, role=MessageRole.AGENT)
        if last_msg:
            response = last_msg.text.value

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()