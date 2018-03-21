from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ios import run_commands
from ansible.module_utils.ios import ios_argument_spec, check_args
import re


def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        count=dict(type="int"),
        dest=dict(type="str", required=True),
        source=dict(type="str"),
        state=dict(type="str", choices=["absent", "present"], default="present"),
        vrf=dict(type="str")
    )

    argument_spec.update(ios_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec)

    count = module.params["count"]
    dest = module.params["dest"]
    source = module.params["source"]
    vrf = module.params["vrf"]

    warnings = list()
    check_args(module, warnings)

    results = {}
    if warnings:
        results["warnings"] = warnings

    results["commands"] = [build_ping(dest, count, source, vrf)]

    ping_results = run_commands(module, commands=results["commands"])
    ping_results_list = ping_results[0].split("\n")

    success, rx, tx, rtt = parse_ping(ping_results_list[3])
    loss = abs(100 - int(success))
    results["packet_loss"] = str(loss) + "%"
    results["packets_rx"] = int(rx)
    results["packets_tx"] = int(tx)

    # Convert rtt values to int
    for k, v in rtt.items():
        if rtt[k] is not None:
            rtt[k] = int(v)

    results["rtt"] = rtt

    validate_results(module, loss, results)

    module.exit_json(**results)


def build_ping(dest, count=None, source=None, vrf=None):
    """
    Function to build the command to send to the terminal for the switch
    to execute. All args come from the module's unique params.
    """
    if vrf is not None:
        cmd = "ping {0} {1}".format(vrf, dest)
    else:
        cmd = "ping {0}".format(dest)

    if count is not None:
        cmd += " repeat {0}".format(str(count))

    if source is not None:
        cmd += " source {0}".format(source)

    return cmd


def parse_ping(ping_stats):
    """
    Function used to parse the statistical information from the ping response.
    Example: "Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/8 ms"
    Returns the percent of packet loss, recieved packets, transmitted packets, and RTT dict.
    """
    rate_re = re.compile("^\w+\s+\w+\s+\w+\s+(?P<pct>\d+)\s+\w+\s+\((?P<rx>\d+)\/(?P<tx>\d+)\)")
    rtt_re = re.compile(".*,\s+\S+\s+\S+\s+=\s+(?P<min>\d+)\/(?P<avg>\d+)\/(?P<max>\d+)\s+\w+\s*$|.*\s*$")

    rate = rate_re.match(ping_stats)
    rtt = rtt_re.match(ping_stats)

    return rate.group("pct"), rate.group("rx"), rate.group("tx"), rtt.groupdict()


def validate_results(module, loss, results):
    """
    This function is used to validate whether the ping results were unexpected per "state" param.
    """
    state = module.params["state"]
    if state == "present" and loss == 100:
        module.fail_json(msg="Ping failed unexpectedly", **results)
    elif state == "absent" and loss < 100:
        module.fail_json(msg="Ping succeeded unexpectedly", **results)


if __name__ == "__main__":
    main()
