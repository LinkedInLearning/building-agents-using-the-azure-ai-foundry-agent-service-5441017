import logging
import json
import azure.functions as func

# Create the Azure Function app instance
app = func.FunctionApp()

@app.function_name(name="QueueFunc")
# Define the queue trigger and output bindings
@app.queue_trigger(arg_name="msg", queue_name="azure-function-input", connection="STORAGE_CONNECTION")
@app.queue_output(arg_name="outputQueue", queue_name="azure-function-output", connection="STORAGE_CONNECTION")
def queue_trigger(msg: func.QueueMessage, outputQueue: func.Out[str]):
    """
    Azure Function triggered by a message in the 'azure-function-input' queue.
    Processes the message and sends a result to the 'azure-function-output' queue.
    """
    try:
        # Decode and parse the incoming queue message
        messagepayload = json.loads(msg.get_body().decode("utf-8"))
        logging.info(f'Received message: {json.dumps(messagepayload)}')

        # Extract required fields from the message
        location = messagepayload.get("location")
        correlation_id = messagepayload.get("CorrelationId")
       
        # Validate required fields
        if not location or not correlation_id:
            raise ValueError("Missing 'location' or 'CorrelationId' in message payload")

        # In a real-world scenario, you'd integrate with a weather API.
        # Here, we'll mock the response.
        mock_weather_data = {
            "New York": "Sunny, 25°C Source: Azure Function", 
            "London": "Cloudy, 18°C Source: Azure Function", 
            "Tokyo": "Rainy, 22°C Source: Azure Function"
        }
        
        weather = mock_weather_data.get(location, "Weather data not available for this location. Source: Azure Function")

        # Prepare the response message    
        response_message = {
            "Value": weather,
            "CorrelationId": correlation_id
        }

        # Log and send the response to the output queue
        logging.info(f'Returning message to output queue: {json.dumps(response_message)}')
        outputQueue.set(json.dumps(response_message))

    except Exception as e:
        # Log any errors that occur during processing
        logging.error(f"Error processing message: {e}")
