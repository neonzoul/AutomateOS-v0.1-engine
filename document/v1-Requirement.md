### **Requirements for `AutomateOS v0.1` (Core Engine MVP)**

This document outlines the functional, non-functional, and technical requirements for the successful completion of the project's first version.

---

### ## Functional Requirements

What the system must be able to do.

#### **1. User & Authentication**

-   The system **must** allow new users to register with an email and password.
-   Passwords **must** be securely hashed before being stored in the database.
-   Registered users **must** be able to log in to receive a JWT access token.
-   The system **must** protect critical API endpoints, requiring a valid JWT for access.

#### **2. Workflow Management (CRUD)**

-   An authenticated user **must** be able to create, read, update, and delete their own workflow definitions via API endpoints.
-   A workflow definition **must** contain a sequence of nodes and their specific configurations (e.g., URL for an HTTP node).

#### **3. Asynchronous Execution Engine**

-   Each workflow **must** have a unique, persistent webhook URL for triggering.
-   When the webhook URL receives a request, the API **must** immediately queue a job for background processing and return a `202 Accepted` status. It **must not** execute the workflow within the API request.
-   A background worker process **must** consume jobs from the queue and execute the workflow logic.
-   The engine **must** process nodes sequentially, passing the output of one node as the input to the next (state management).

#### **4. Core Nodes**

-   The system **must** include a functional **HTTP Request Node** capable of making GET and POST requests.
-   The system **must** include a functional **Filter Node** capable of conditionally continuing or halting the workflow based on input data.

#### **5. Logging & History**

-   The system **must** record the history for each workflow execution, including its status (Success, Failed, In-Progress), start time, and end time.
-   A user **must** be able to retrieve their workflow execution history via an API endpoint.

---

### ## Non-Functional Requirements

How the system should operate and be built.

-   **Security:** Sensitive information, such as user passwords and credentials for nodes, **must** be encrypted/hashed at rest.
-   **Maintainability:** The node system **must** be designed as a **Plugin Architecture**. Adding a new node type should not require modifying the core engine's execution loop.
-   **Performance:** The API layer **must** have a fast response time for queuing jobs (target < 200ms).

---

### ## Technical Stack

The required technologies for this implementation.

-   **Backend:** Python (3.10+), FastAPI
-   **Database:** SQLModel (ORM), PostgreSQL (for production), SQLite (for local development)
-   **Job Queuing:** Redis, RQ (Redis Queue)
-   **Deployment:** Docker, Docker Compose

---

### ## Deliverables (Definition of "Done")

The final artifacts that must be produced by the end of the 6-week sprint.

1.  A complete source code repository on GitHub.
2.  A `docker-compose.yml` file that starts the entire application stack (API, Worker, DB, Redis) with a single command.
3.  Auto-generated API documentation via FastAPI.
4.  A `README.md` file explaining the project and how to set it up locally.
