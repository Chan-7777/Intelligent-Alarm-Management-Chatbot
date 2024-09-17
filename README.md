Ausura 😎 - Intelligent Alarm Management Chatbot

Overview
Ausura is an intelligent chatbot designed to assist with alarm management in industrial plants. It leverages advanced language models to provide real-time insights and responses based on critical alarm data. The chatbot is built using the LangChain framework, integrated with AWS services, and deployed via Streamlit for an interactive user interface.

Key Features
- Real-Time Alarm Insights: Provides detailed information about critical alarms in various plants, including alarm names, equipment affected, and criticality levels.
- Context-Aware Conversations: Automatically attaches relevant alarm context to user queries, ensuring accurate and contextually relevant responses.
- Multiple Language Models: Supports different language models, including `anthropic.claude-3-haiku-20240307-v1:0` and `meta.llama3-8b-instruct-v1:0`, allowing users to select the model that best fits their needs.
- Memory Management: Utilizes `ConversationSummaryBufferMemory` to maintain context across interactions, ensuring coherent and continuous conversations.
- User-Friendly Interface: Deployed using Streamlit, providing an intuitive and interactive interface for users to interact with the chatbot.

Technical Details
- Backend: 
  - LangChain: Utilizes LangChain's `ConversationChain` and `ConversationSummaryBufferMemory` for managing conversations and memory.
  - AWS Integration: Uses `ChatBedrock` from `langchain_aws` to interact with AWS services for model deployment and prompt management.
  - Boto3: Employed for accessing and retrieving prompt templates from AWS S3.
  - JSON Handling: Loads and processes alarm data from JSON files stored in S3.

- Frontend:
  - Streamlit: Provides a web-based interface for users to interact with the chatbot.
  - Dynamic Model Selection: Allows users to select the desired language model from a dropdown menu.
  - Chat History: Maintains and displays the chat history for ongoing conversations.

How It Works
1. Initialization: The chatbot and memory are initialized based on the selected language model.
2. Context Attachment: User input is processed to attach relevant alarm context based on keywords and plant names.
3. Conversation Management: The chatbot processes the input, generates a response using the selected language model, and maintains the conversation context.
4. User Interaction: Users interact with the chatbot through the Streamlit interface, receiving real-time responses and insights.

Use Cases
- Industrial Alarm Management: Provides plant operators and managers with real-time insights into critical alarms, helping them make informed decisions.
- Training and Support: Acts as a training tool for new employees, providing detailed explanations and context for various alarms and their criticality.
- Automation: Automates the process of alarm monitoring and management, reducing the need for manual intervention.
