# Empty Container Repositioning (ECR)

The Empty Container Repositioning (ECR) scenario simulates a common problem of
container shipping in marine transportation. Imagine an international market:
The goods are packed in containers and shipped by vessels from the exporting
country to the importing country. As a result of the imbalanced global trade,
the volume of available containers in different ports may not match their needs.
In other words, some ports will have excess containers while some ports may be
in short. Therefore, We can use the excess capacity on vessels to reposition
empty containers to alleviate this imbalance.

## Resource Flow

In this scenario, the **container** is the central resource. Two events will
trigger the movement of the container:

- The first one is the order, which will lead to the transportation of goods from
the source port to the destination port.
- The second one is the repositioning operation. It is used to rebalance the
container distribution worldwide.

![The Life Cycle of the Container](../images/scenario/ecr.container_flow.svg)

### Order

To simulate a real market, we assume that there will be a certain number of orders
from some ports to other ports every day. And the total order number of each day
is generated according to a predefined distribution. These orders are then allocated
to each export port in a relatively fixed proportion, and each export port will
have a relatively fixed number of import ports as customers. The order distribution
and the proportion of order allocation are specified in the topology and can be
customized based on different requirements.

An order will trigger a life cycle of a container, as shown in the figure above,
a life cycle is defined as follows:

- Once an order is generated, an empty container of the corresponding export port
(source port) will be released to the shipper.
- The shipper will fill the container with cargo which turns it into a laden and
then return it to the port after a few days.
- Loading occurs when the vessel arrives at this port.
- After several days of sailing, the vessel will finally arrive at the corresponding
import port (destination port) where the discharging of the laden happens.
- Then the laden will be released to the consignee, and the consignee will take
out the cargo in it, which turns it into an empty container again.
- Finally, the consignee returns it as an available container for the import port
in a few days.

### Container Repositioning

As mentioned above, to rebalance the container distribution, the agent in each
port will decide how to reposition the empty containers every time a vessel
arrives at the port. The decision consists of two parts:

- Whether to take a `discharge` operation or a `load` operation;
- The number of containers to discharge/load.

The export-oriented ports (e.g. the ports in China) show a clearly high demand
feature, and usually require additional supply of empty containers. These ports
will tend to discharge empty containers from the vessel if feasible. While the
import-oriented ports have a significant surplus feature, that usually receive
many empty container from the consignee. So the imported-oriented ports will tend
to load the surplus empty containers into the vessel if there is free capacity.

The specific quantity to operate for a `discharge` action is limited by the
remaining space in the port and the total number of empty containers in the vessel.
Similarly, a `load` action is limited by the remaining space in the vessel and
the total number of empty containers in the port. Of course, a good decision will
not only consider the self future supply and demand situation, but also the needs
and situation of the upstream and downstream ports.

## Topologies

To provide an exploration road map from easy to difficult, two kinds of topologies
are designed and provided in ECR scenario. Toy topologies provide simplified
environments for algorithm debugging and will show some typical relationships
between ports to users. We hope these will provide users with some insights to
know more and deeper about this scenario. While the global topologies are based
on the real-world data, and are bigger and more complicated to present the real
problem.

### Toy Topologies

![ECR toy topologies](../images/scenario/ecr.toys.svg)

*(In these topologies, the solid lines indicate the service route (voyage) among
ports, while the dashed lines indicate the container flow triggered by orders.)*

**toy.4p_ssdd_l0.D**: There are four ports in this topology. According to the orders,
D1 and D2 are simple demanders (the port requiring additional empty containers)
while S2 is a simple supplier (the port with surplus empty containers). Although
S1 is a simple destination port, it's at the intersection of two service routes,
which makes it a special port in this topology. To achieve the global optimum,
S1 must learn to distinguish the service routes and take service route specific
repositioning operations.

**toy.5p_ssddd_l0.D**: There are five ports in this topology. According to the orders,
D1 and D2 are simple demanders while S1 and S2 are simple suppliers. As a port
in the intersection of service routes, although the supply and demand of port T1
can reach a state of self-balancing, it still plays an important role for the
global optimum. The best repositioning policy for port T1 is to transfer the
surplus empty containers from the left service route to the right one. Also, the
port D1 and D2 should learn to discharge only the quantity they need and leave the
surplus ones to other ports.

**toy.6p_sssbdd_l0.D**: There are six ports in this topology. Similar to toy.5p_ssddd,
in this topology, there are simple demanders D1 and D2, simple suppliers S1 and
S2, and self-balancing ports T1 and T2. More difficult than in toy.5p_ssddd,
more transfers should be taken to reposition the surplus empty containers from
the left most service route to the right most one, which means a multi-steps
solution that involving more ports is required.

### Global Topologies

**global_trade.22p_l0.D**: This is a topology designed based on the real-world data.
The order generation model in this topology is built based on the trade data from
[WTO](https://data.wto.org/). According to the query results in WTO from January
2019 to October 2019, The ports with large trade volume are selected, and the
proportion of each port as the source of orders is directly proportional to the
export volume of the country it belongs to, while the proportion as the destination
is proportional to the import volume. While the service routes among the selected
ports in this topology are following the service routes provided by
[OOCL](https://www.oocl.com/eng/ourservices/serviceroutes/Pages/default.aspx).
In this scenario, there are much more ports, much more service routes. And most
ports no longer have a simple supply/demand feature. The cooperation among ports
is much more complex and it is difficult to find an efficient repositioning policy
manually.

![global_trade.22p](../images/scenario/ecr.global_trade.svg)

*(To make it clearer, the figure above only shows the service routes among ports.)*

### Naive Baseline

Below are the performance of *no repositioning* and *random repositioning* in
different topologies. The performance metric used here is the *fulfillment ratio*.

| Topology         | No Repositioning | Random Repositioning |
| :--------------: | :--------------: | :------------------: |
| toy.4p_ssdd_l0.0 | 11.16 +/- 0.00   | 36.76 +/-  3.19      |
| toy.4p_ssdd_l0.1 | 11.16 +/- 0.00   | 78.42 +/-  5.67      |
| toy.4p_ssdd_l0.2 | 11.16 +/- 0.00   | 71.37 +/- 12.51      |
| toy.4p_ssdd_l0.3 | 11.16 +/- 0.00   | 67.37 +/- 11.60      |
| toy.4p_ssdd_l0.4 | 11.16 +/- 0.03   | 68.99 +/- 12.11      |
| toy.4p_ssdd_l0.5 | 11.16 +/- 0.03   | 67.07 +/- 12.81      |
| toy.4p_ssdd_l0.6 | 11.16 +/- 0.03   | 67.90 +/-  4.44      |
| toy.4p_ssdd_l0.7 | 11.16 +/- 0.03   | 62.13 +/-  5.82      |
| toy.4p_ssdd_l0.8 | 11.17 +/- 0.03   | 64.05 +/-  5.16      |

| Topology          | No Repositioning | Random Repositioning |
| :---------------: | :--------------: | :------------------: |
| toy.5p_ssddd_l0.0 | 22.32 +/- 0.00   | 57.15 +/- 4.38       |
| toy.5p_ssddd_l0.1 | 22.32 +/- 0.00   | 64.15 +/- 3.91       |
| toy.5p_ssddd_l0.2 | 22.32 +/- 0.00   | 64.14 +/- 3.54       |
| toy.5p_ssddd_l0.3 | 22.33 +/- 0.00   | 64.37 +/- 3.87       |
| toy.5p_ssddd_l0.4 | 22.32 +/- 0.06   | 63.53 +/- 3.93       |
| toy.5p_ssddd_l0.5 | 22.32 +/- 0.06   | 63.93 +/- 3.72       |
| toy.5p_ssddd_l0.6 | 22.32 +/- 0.06   | 54.60 +/- 5.40       |
| toy.5p_ssddd_l0.7 | 22.32 +/- 0.06   | 45.00 +/- 6.05       |
| toy.5p_ssddd_l0.8 | 22.34 +/- 0.06   | 46.32 +/- 4.96       |

| Topology           | No Repositioning | Random Repositioning |
| :----------------: | :--------------: | :------------------: |
| toy.6p_sssbdd_l0.0 | 34.15 +/- 0.00   | 44.69 +/- 6.84       |
| toy.6p_sssbdd_l0.1 | 34.15 +/- 0.00   | 59.35 +/- 5.11       |
| toy.6p_sssbdd_l0.2 | 34.15 +/- 0.00   | 59.35 +/- 4.97       |
| toy.6p_sssbdd_l0.3 | 34.16 +/- 0.00   | 56.69 +/- 4.45       |
| toy.6p_sssbdd_l0.4 | 34.14 +/- 0.09   | 56.72 +/- 4.37       |
| toy.6p_sssbdd_l0.5 | 34.14 +/- 0.09   | 56.13 +/- 4.34       |
| toy.6p_sssbdd_l0.6 | 34.14 +/- 0.09   | 56.76 +/- 1.52       |
| toy.6p_sssbdd_l0.7 | 34.14 +/- 0.09   | 55.86 +/- 2.70       |
| toy.6p_sssbdd_l0.8 | 34.18 +/- 0.09   | 55.36 +/- 2.11       |

| Topology              | No Repositioning | Random Repositioning |
| :-------------------: | :--------------: | :------------------: |
| global_trade.22p_l0.0 | 68.57 +/- 0.00   | 59.27 +/- 1.56       |
| global_trade.22p_l0.1 | 66.64 +/- 0.00   | 64.56 +/- 0.70       |
| global_trade.22p_l0.2 | 66.55 +/- 0.00   | 64.73 +/- 0.57       |
| global_trade.22p_l0.3 | 65.24 +/- 0.00   | 63.31 +/- 0.68       |
| global_trade.22p_l0.4 | 65.22 +/- 0.15   | 63.46 +/- 0.76       |
| global_trade.22p_l0.5 | 64.90 +/- 0.15   | 63.10 +/- 0.79       |
| global_trade.22p_l0.6 | 63.74 +/- 0.49   | 60.98 +/- 0.50       |
| global_trade.22p_l0.7 | 60.14 +/- 0.47   | 56.38 +/- 0.75       |
| global_trade.22p_l0.8 | 60.17 +/- 0.45   | 56.45 +/- 0.67       |

<!-- ## Quick Start

### Data Preparation

### Environment Interface

#### DecisionEvent

Once the environment need the agent's response to promote the simulation, it will throw an **DecisionEvent**. In the scenario of ECR, the information of each DecisionEvent is listed as below:

- **tick**: (int) the corresponding tick
- **port_idx**: (int) the id of the port/agent that needs to respond to the environment
- **vessel_idx**: (int) the id of the vessel/operation object of the port/agnet.
- **snapshot_list**: (int) **Snapshots of the environment to input into the decision model** TODO: confirm the meaning
- **action_scope**: **Load and discharge scope for agent to generate decision**
- **early_discharge**: **Early discharge number of corresponding vessel**

#### Action

Once we get a DecisionEvent from the environment, we should respond with an Action. Valid Action could be:

- None, which means do nothing.
- A valid Action instance, including:
  - **vessel_idx**: (int) the id of the vessel/operation object of the port/agent.
  - **port_idx**: (int) the id of the port/agent that take this action.
  - **quantity**: (int) the sign of this value denotes different meanings:
    - positive quantity means unloading empty containers from vessel to port.
    - negative quantity means loading empty containers from port to vessel.

### Example (Random Action)

```python
from maro.simulator import Env
from maro.simulator.scenarios.ecr.common import Action

start_tick = 0
durations = 100  # 100 days

# Initialize an environment with a specific scenario, related topology.
env = Env(scenario="ecr", topology="5p_ssddd_l0.0",
          start_tick=start_tick, durations=durations)

# Query environment summary, which includes business instances, intra-instance attributes, etc.
print(env.summary)

for ep in range(2):
    # Gym-like step function
    metrics, decision_event, is_done = env.step(None)

    while not is_done:
        past_week_ticks = [x for x in range(
            decision_event.tick - 7, decision_event.tick)]
        decision_port_idx = decision_event.port_idx
        intr_port_infos = ["booking", "empty", "shortage"]

        # Query the decision port booking, empty container inventory, shortage information in the past week
        past_week_info = env.snapshot_list["ports"][past_week_ticks:
                                                    decision_port_idx:
                                                    intr_port_infos]

        dummy_action = Action(decision_event.vessel_idx,
                              decision_event.port_idx, 0)

        # Drive environment with dummy action (no repositioning)
        metrics, decision_event, is_done = env.step(dummy_action)

    # Query environment business metrics at the end of an episode, it is your optimized object (usually includes multi-target).
    print(f"ep: {ep}, environment metrics: {env.get_metrics()}")
    env.reset()
```

Detail link -->
