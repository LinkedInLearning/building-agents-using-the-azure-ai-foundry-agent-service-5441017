# Deployment and Usage Instructions for Azure Function (Queue Trigger)

## 1. Prepare Your Files

- Ensure your folder contains:
  - `function_app.py` (your function code)
  - `requirements.txt`
  - `host.json`

## 2. Create Queues in Azure Storage

1. Go to your Storage Account in the Azure Portal.
2. In the left menu, select **Queues** under "Data storage".
3. Click **+ Queue** and create:
   - `azure-function-input`
   - `azure-function-output`

## 3. Create an Azure Function App

1. In the Azure Portal, click **Create a resource** > **Function App**.
2. Choose Python as the runtime stack.
3. Select your subscription, resource group, and region.
4. Link to your Storage Account.
5. Complete the creation steps.

## 4. Set the STORAGE_CONNECTION Application Setting

1. In your Function App, go to **Environment Variables** (under "Settings").
2. Click **+ Add**.
3. Name: `STORAGE_CONNECTION`
4. Value: (Paste your Storage Account connection string)
5. Click **Apply** and **Save**.

## 5. Zip and Deploy Your Function

1. Zip the contents of your function app folder (not the folder itself, just the 3 files).
2. In the GitHub Codespaces terminal run the following code:
az functionapp deployment source config-zip -g <resource group> -n <function app name> --src functionapp.zip

## 6. Verify and Test

1. In the Function App, check the **Functions** blade to see your function listed.
2. Add a test message to the `azure-function-input` queue (use Azure Portal, Storage Explorer, or code).
   - Example message:
     ```json
     {
       "location": "London"
     }
     ```
3. Check the `azure-function-output` queue for the processed result.

## 7. Monitor and Troubleshoot

- Use the **Logs** and **Monitor** sections in the Function App to view execution logs and troubleshoot any issues.
