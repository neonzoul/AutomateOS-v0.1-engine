# Worker Task that Use Orchestrator.
from sqlmodel import Session

from app.db.session import engine # For worker use
from app.models.workflow import Workflow, WorkflowRun
from app.engine.orchestrator import run_workflow


def process_workflow(workflow_id: int):
    """
    The main task executed by the RQ worker.
    It fetches a workflow from the database and passes it to the orchestrator.
    """
    print(f"WORKER: Received job. Processing workflow ID: {workflow_id}")
    
    # "Worker-Side Database Session"
    with Session(engine) as session:
        # Fetch the workflow definition from the database with primary_key.
        workflow = session.get(Workflow, workflow_id)

        if not workflow:
            print(f"WORKER: Error - Workflow with ID {workflow_id} not found.")
            return
        
        # Create a new WorkflowRun recoed to track this execution.
        run_log = WorkflowRun(workflow_id=workflow_id, status="In-Progress", logs={})
        session.add(run_log)
        session.commit()
        session.refresh(run_log)

        try:
            # Call the orchestrator to run the workflow.
            final_output = run_workflow(workflow.definition)

            run_log.status = "Success"
            run_log.logs = {"final_output": final_output}
            print(f"WORKER: Successfully process workflow ID: {workflow_id}")

        except Exception as e:
            run_log.status = "Failed"
            run_log.logs = {"error": str(e)}

            print(f"WORKER: Failed to process workflow ID: {workflow_id}. Error: {e}")

        finally:
            # Commit the final status (either "Sucess" or "Failed")
            session.add(run_log)
            session.commit()