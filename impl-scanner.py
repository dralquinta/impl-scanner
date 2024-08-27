from google.cloud import compute_v1

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
        print(f"VPC Subnets: {[subnet.name for subnet in network.subnetworks]}")

        if network.peerings:
            print("Peering Connections:")
            for peering in network.peerings:
                print(f"  - Peering Name: {peering.name}")
                print(f"  - Peering Network: {peering.network}")
                print(f"  - Peering State: {peering.state}")
        else:
            print("No Peering Connections")

        print("---")

if __name__ == "__main__":
    project_id = "maps-dryrun"  # Replace with your actual project ID
    list_vpcs_and_connections(project_id)