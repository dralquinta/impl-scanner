from google.cloud import compute_v1
from google.cloud import recommender_v1
import time
from diagrams import Diagram, Cluster, Edge

def list_vpcs_and_connections(project_id):
    """
    Lists VPCs in the specified project, identifies peering connections, and returns data for diagramming.
    """

    client = compute_v1.NetworksClient()
    request = compute_v1.ListNetworksRequest()
    request.project = project_id

    response = client.list(request=request)

    vpc_data = {}  # Dictionary to store VPC and peering data

    for network in response:
        vpc_name = network.name
        vpc_data[vpc_name] = {
            'subnets': [subnet.name for subnet in network.subnetworks] if isinstance(network.subnetworks, list) else network.subnetworks,
            'peerings': [(peering.name, peering.network) for peering in network.peerings]
        }

        # ... (Existing print statements for console output can remain if desired) ...

    return vpc_data

def generate_vpc_diagram(vpc_data):
    """
    Generates a VPC network diagram using the 'diagrams' library.
    """

    with Diagram("GCP VPC Network", show=False):  # Diagram context
        for vpc_name, vpc_info in vpc_data.items():
            with Cluster(vpc_name):  # VPC cluster
                for subnet in vpc_info['subnets']:
                    # Subnet representation (customize as needed)
                    subnet_node = f"{subnet} (subnet)" 

            for peering_name, peering_network in vpc_info['peerings']:
                # Peering connection (adjust styling as desired)
                Edge(vpc_name, peering_network, label=peering_name)

if __name__ == "__main__":
    project_id = "maps-dryrun"
    vpc_data = list_vpcs_and_connections(project_id)
    generate_vpc_diagram(vpc_data)