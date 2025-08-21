"""The Orchestrator that dynamically loads and runs the nodes."""
from __future__ import annotations

import importlib # [[to achieve dynamuc loading.]]
from typing import Any, Dict

def run_workflow(workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dynamically loads and executes the nodes defined in a workflow.
    """
    print(f"Orchestrator: Starting workflow run...")

    # This variable will hold the output of one node to be the input of the next.
    current_data: Dict[str, Any] = {}

    # Loop through each step defined in the workflow
    for step in workflow_definition.get("steps", []):
        node_type = step.get("type")
        node_config = step.get("config", {})

        if not node_type:
            continue # or raise an error

        try:
            # 1. Dynamically import the node's module
            module_path = f'app.engine.nodes.{node_type}'
            node_module = importlib.import_module(module_path)

            # 2. Find the class within the module
            # Use a convention: The class is CamelCase version of the file name.
            #[[ e.g., http_request_node.py -> HttpRequestNode ]]
            class_name = "".join(word.capitalize() for word in node_type.split("_"))
            NodeClass = getattr(node_module, class_name)

            # 3. Create an instance & execute it
            node_instance = NodeClass(config=node_config)
            current_data = node_instance.execute(input_data=current_data)

            print(f"Orchestrator: Successfully executed node '{node_type}'.")
        
        except (ImportError, AttributeError) as e:
            print(f"Orchestrator: Error loading or running node '{node_type}': {e}")
            raise

    print(f"Orchestrator: Workflow run finished.")
    return current_data
            

