from google.cloud import compute_v1
from google.cloud import recommender_v1
import time

def list_vpcs_and_connections(project_id):
    """
    Lists VPCs in the specified project and identifies peering connections.
    """

    client = compute_v1.NetworksClient()
    request = compute_v1.ListNetworksRequest()
    request.project = project_id

    response = client.list(request=request)

    for network in response:
        print(f"VPC Name: {network.name}")
        print(f"VPC ID: {network.id}")
        print(f"VPC Description: {network.description}")

        # Enhanced Subnet Handling
        if isinstance(network.subnetworks, list): 
            print(f"VPC Subnets: {[subnet.name for subnet in network.subnetworks]}")
        else:
            print(f"VPC Subnets: {network.subnetworks}") 

        if network.peerings:
            print("Peering Connections:")
            for peering in network.peerings:
                print(f"  - Peering Name: {peering.name}")
                print(f"  - Peering Network: {peering.network}")
                print(f"  - Peering State: {peering.state}")
        else:
            print("No Peering Connections")

        print("---")

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

if __name__ == "__main__":
    project_id = "maps-dryrun" 
    list_vpcs_and_connections(project_id)
   #poll_recommendations(project_id)