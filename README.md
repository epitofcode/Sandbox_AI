```mermaid
graph TD
    subgraph Phase 1: Initial Setup & Configuration
        A1[Start] --> A2{Create Google Cloud Project};
        A2 --> A3{Enable Vertex AI API};
        A3 --> A4[Create OAuth 2.0 Client ID];
        A4 -- using 'http://localhost:3000' --> A5[Get Client ID & Secret];
        A3 --> A6[Create Service Account];
        A6 --> A7[Download Service Account JSON Key];
        A5 & A7 --> A8[(Store All Credentials Securely)];
    end

    subgraph Phase 2: Backend & Data Pipeline Development (Python/FastAPI)
        B1[Initialize FastAPI Project] --> B2{Implement SSO/OAuth Login Endpoint};
        B2 -- uses Client ID/Secret --> B3[Handle User Login & Get User OAuth Token];
        B3 --> B4{Develop Data Connectors};
        B4 --> B5[Connector: Google Drive API];
        B4 --> B6[Connector: Gmail API];
        B4 --> B7[Connector: Notion API];
        B4 --> B8[Connector: HubSpot API];
        
        subgraph Per-Connector Logic
            B5 -- uses User Token --> B9{Fetch Data (e.g., files)};
            B6 -- uses User Token --> B9;
            B7 -- uses User Token --> B9;
            B8 -- uses User Token --> B9;
            B9 --> B10[Extract & Clean Text];
            B10 --> B11[Chunk Text into Smaller Pieces];
        end

        B11 --> B12{Upload Processed Chunks to Vertex AI};
        B12 -- authenticates w/ Service Account Key --> B13((Vertex AI RAG Engine));
        B13 -- "Auto-Creates Embeddings & Index" --> B14([Indexed Knowledge Base]);
        
        B1[Initialize FastAPI Project] --> B15{Create '/chat' API Endpoint};
    end

    subgraph Phase 3: Frontend Development (React.js)
        C1[Initialize React App] --> C2{Create UI Components};
        C2 --> C3[Login Button];
        C2 --> C4[Chat Window & Input Box];
        C3 --> C5{Implement Login Flow};
        C5 -- "onClick" --> C6[Redirects User to Google for Auth];
    end

    subgraph Phase 4: Final Application Workflow
        D1[User Opens Web App at 'localhost:3000'] --> D2{User Clicks Login Button};
        D2 -- from Frontend --> C6;
        C6 --> D3{User Authenticates with Google};
        D3 --> D4[Google Redirects to '/auth/callback'];
        D4 -- "sends auth code to Backend" --> B3;
        B3 --> D5[User is Logged In];

        D5 --> D6{User Types Question & Hits Send};
        D6 -- "sends question to /chat endpoint" --> B15;
        B15 -- "queries RAG Engine with question" --> B13;
        B13 -- "Retrieves relevant text from" --> B14;
        B13 -- "Generates answer with LLM" --> D7[LLM Response];
        D7 -- "streamed back from Backend" --> D8{Frontend Displays Answer};
        D8 --> D6;
    end

    %% Styling and Linking
    linkStyle 0 stroke:#007bff,stroke-width:2px;
    linkStyle 1,2,3,4,5,6 stroke:#28a745,stroke-width:2px;
    linkStyle 16,17,18,25 stroke:#ffc107,stroke-width:2px;
    linkStyle 26,27,28,29,30,31,32,33,34 stroke:#17a2b8,stroke-width:2px;




### How to Read the Flowchart:

1.  **Phase 1 (Blue):** This is the one-time setup you need to do in the Google Cloud Console to get your keys and credentials.
2.  **Phase 2 (Green):** This represents the bulk of your backend Python coding: setting up the server, handling logins, building the data pipeline to pull data from sources, and sending it to Vertex AI.
3.  **Phase 3 (Yellow):** This covers the frontend work in React to build the user interface.
4.  **Phase 4 (Cyan):** This illustrates the complete end-to-end flow from the user's perspective when they interact with your finished application. It shows how the frontend and backend work together to answer a question.