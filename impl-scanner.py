from google.cloud import asset_v1
from googleapiclient import discovery
import graphviz
import google.auth

# Authentication - The Key to the Kingdom

credentials, project_id = google.auth.default()

# 1. Data Collection - The Grand Inquisition

def fetch_resources_from_cai(organization_id):
    """Fetches resources from Cloud Asset Inventory."""
    client = asset_v1.AssetServiceClient(credentials=credentials)
    scope = f'organizations/{organization_id}'
    page_size = 1000  # Adjust as needed
    page_token = None

    while True:
        response = client.search_all_resources(
            scope=scope,
            query="*",
            page_size=page_size,
            page_token=page_token
        )
        for resource in response:
            yield resource
        page_token = response.next_page_token
        if not page_token:
            break

def fetch_networks_from_compute_api(project_id):
    """Fetches networks using the Compute Engine API."""
    compute = discovery.build('compute', 'v1', credentials=credentials)
    request = compute.networks().list(project=project_id)
    networks = []
    while request is not None:
        response = request.execute()
        networks.extend(response.get('items', []))
        request = compute.networks().list_next(previous_request=request, previous_response=response)
    return networks

# 2. Data Processing & Visualization - The Mastermind's Canvas

def build_graph(resources, networks):
    """Constructs a Graphviz graph from collected data."""
    dot = graphviz.Digraph(comment='GCP Organization Architecture', strict=True)

    # 2.1 Hierarchy 
    for resource in resources:
        if resource.asset_type == 'cloudresourcemanager.googleapis.com/Project':
            dot.node(resource.name, resource.display_name, shape='box') 

    # 2.2 Networking
    for network in networks:
        project_id = network['selfLink'].split('/')[-3]
        dot.node(network['name'], network['name'], shape='ellipse')
        dot.edge(project_id, network['name'])

    # 2.3 Resource Relationships - The Interconnected Web
    resource_relationships = {}
    for resource in resources:
        if resource.asset_type == 'compute.googleapis.com/Instance':
            zone = resource.name.split('/')[-3]
            network = resource.additional_attributes.get('network', 'Unknown Network')
            resource_relationships.setdefault(network, []).append((resource.name, zone))
        # ... (Add more resource types and their relationships here)

    for network, instances in resource_relationships.items():
        for instance_name, zone in instances:
            dot.node(instance_name, f"{instance_name}\n({zone})", shape='box')
            dot.edge(network, instance_name)

    # 2.4 IAM - The Gatekeepers
    iam_policies = {}
    for resource in resources:
        if resource.iam_policy:
            iam_policies[resource.name] = resource.iam_policy

    for resource_name, policy in iam_policies.items():
        for binding in policy.bindings:
            for member in binding.members:
                dot.edge(member, resource_name, label=binding.role, style='dashed') 

    return dot






def __exec_orchestrator():
    print("Hi")
    organization_id = 'YOUR_ORGANIZATION_ID' 

    resources = fetch_resources_from_cai(organization_id)
    networks = []
    for resource in resources:
        if resource.asset_type == 'cloudresourcemanager.googleapis.com/Project':
            networks.extend(fetch_networks_from_compute_api(resource.name))

    graph = build_graph(resources, networks)
    graph.render('gcp_architecture', view=True, format='png')
    




def __main__():
    __exec_orchestrator()   


__main__()