def flow_key(record):
    workload = record["workload"]
    destination = record["destination"]
    port = record["port"]
    protocol = record["protocol"]
    if not all(isinstance(value, str) and value for value in (workload, destination)):
        raise ValueError("workload and destination must be non-empty identifiers")
    if type(port) is not int or not 1 <= port <= 65535 or protocol not in ("TCP", "UDP", "SCTP"):
        raise ValueError("flow requires a valid port and an uppercase transport protocol")
    return workload, destination, port, protocol


def evaluate(data, fixture_path):
    approved = {flow_key(record) for record in data["approved"]}
    observed = {flow_key(record) for record in data["observed"]}
    return [{"code": "egress_outside_allowlist", "workload": workload, "destination": destination,
             "port": port, "protocol": protocol}
            for workload, destination, port, protocol in sorted(observed - approved)]
