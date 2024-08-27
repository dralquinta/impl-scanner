from google.cloud import compute_v1
from google.cloud import recommender_v1
import time
import networkx as nx
import matplotlib.pyplot as plt
from diagrams.gcp.compute import VPCNetwork
from diagrams.gcp.network import LoadBalancing

def list_vpcs_and_connections(project_id):
    """
    Lists VPCs in the specified project, identifies peering connections, and returns data for diagramming.
    """

    client = compute_v1.NetworksClient()
    request = compute_v1.ListNetworksRequest()
    request.project = project_id

    response = client.list(request=request)

    vpc_data = {} 

    for network in response:
        vpc_name = network.name
        vpc_data[vpc_name] = {
            'subnets': [subnet.name for subnet in network.subnetworks] if isinstance(network.subnetworks, list) else network.subnetworks,
            'peerings': [(peering.name, peering.network) for peering in network.peerings]
        }

        # ... (Existing print statements for console output can remain if desired) ...

    return vpc_data

def poll_recommendations(project_id):
    """
    Polls for active recommendations related to VPCs in the specified project.
    """

    client = recommender_v1.RecommenderClient()
    parent = f"projects/{project_id}/locations/global/recommenders/google.compute.network.Network"
    request = recommender_v1.ListRecommendationsRequest(
        parent=parent,
        filter="state_info.state=ACTIVE", 
    )

    while True: 
        response = client.list_recommendations(request=request)

        for recommendation in response:
            print(f"Recommendation Name: {recommendation.name}")
            print(f"Description: {recommendation.description}")
            # ... (Extract and print other relevant details as needed) ...
            print("---")

        if not response.recommendations:
            print("No active recommendations found.")

        time.sleep(60) 

def generate_vpc_diagram(vpc_data, output_filename="vpc_network_diagram.png"):
    """
    Generates a VPC network diagram using diagrams with GCP icons.
    """

    with Diagram("GCP VPC Network", filename=output_filename, show=False):
        vpc_nodes = {} 

        for vpc_name in vpc_data.keys():
            vpc_nodes[vpc_name] = VPCNetwork(vpc_name)

        for vpc_name, vpc_info in vpc_data.items():
            for peering_name, peering_network in vpc_info['peerings']:
                Edge(vpc_nodes[vpc_name], vpc_nodes[peering_network], label=peering_name)

    print(f"Diagram saved to {output_filename}")

if __name__ == "__main__":
    project_id = "dryruns" 
    output_filename = "vpc_network_diagram.png" 

    vpc_data = list_vpcs_and_connections(project_id)
    generate_vpc_diagram(vpc_data, output_filename)
   # poll_recommendations(project_id)