#!/usr/bin/env python3
"""
The simulator first creates a Python object for the link (link), a Python
object for modeling the minimum RTT (pdbox), and a Python object to capture the
end hosts, i.e., the sender and the receiver (host).

There is no separate Python object for the sender and for the receiver. Both the
sender and the receiver are implemented within the same Python object called
host. host.send() is called when sending packets and host.recv() is called when
receiving ACKs for the packet an RTT (i.e., minimum RTT + queuing delay) later.

Similarly, there is no separate packet header format for packets and ACKs. They
are one and the same. The acknowledgement process works by calling host.recv()
on the same packet that was sent out as part of a host.send()in the past.

The code connects host to link, link to pdbox, and pdbox to host. Hence,
packets "flow" from host (where the send() method is called to send packets) to
link (where queues build up) to pdbox (where the packets incur a min.RTT worth
of delay) back to host (where the recv() method is called to process ACKs for
packets that were sent by host.send()).

The current value of time is represented by the variable tick, which is set in
the for loop and then passed to each of the objects within the simulator. If you
need to access the current value of time when implementing a protocol (e.g., for
computing RTT samples, or for setting the timestamp at which a packet was sent),
tick is the variable you should be using. You don't need to create your own
version of time.
"""

import argparse
import random
from network import DelayBox, Link
from packet import Packet
from timeout_calculator import TimeoutCalculator
from stop_and_wait_host import StopAndWaitHost
from sliding_window_host import SlidingWindowHost
from aimd_host import AimdHost


def check_host_type(host_type):
    # Check that host_type is one of three strings
    if host_type.lower() not in ["stopandwait", "slidingwindow", "aimd"]:
        raise argparse.ArgumentTypeError(
            "Invalid host_type, must be StopAndWait or SlidingWindow or AIMD"
        )
    return host_type.lower()


class Simulator:
    def __init__(
        self, host, loss_ratio, queue_limit, rtt_min, seed, verbose=True
    ):
        self.host = host
        # Initialize the random seed so that it is deterministic
        random.seed(seed)
        # Construct the different elements

        # The network link connecting sender to the receiver
        # In the simulation, the sender and receiver are really the same object (host),
        # and correspond to the send() and recv() methods
        self.link = Link(
            loss_ratio=loss_ratio, queue_limit=queue_limit, verbose=verbose
        )

        # Create a box representing the two-way propagation delay
        # , i.e., the minimum round-trip time
        if rtt_min < 2:
            raise argparse.ArgumentTypeError("rtt_min must be at least 2")
        self.pdbox = DelayBox(rtt_min - 1)

    def send(self, tick_val):
        # Let the host associated with this link generate a packet
        return self.host.send(tick_val)

    def tick(self, tick_val):
        # Run the simulation for the specified number of ticks,
        # by running the host, then the link, then the pdbox
        packets = self.send(tick_val)
        if packets is not None:
            # If a single packet is received, convert it to list
            if type(packets) is Packet:
                packets = [packets]

            # Transmit the packets received from the host
            for packet in packets:
                self.link.recv(packet)

        self.link.tick(tick_val, self.pdbox)
        self.pdbox.tick(tick_val, self.host)


if __name__ == "__main__":
    # Usage for command line arguments
    parser = argparse.ArgumentParser(
        description="Assignment 2 simulator. Link capacity is always 1 packet per tick"
    )
    optional = parser._action_groups.pop()

    # required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="random seed to make sim. deterministic",
        required=True,
    )
    required.add_argument(
        "--host_type",
        dest="host_type",
        type=check_host_type,
        choices=["stopandwait", "slidingwindow", "aimd"],
        required=True,
    )
    required.add_argument(
        "--rtt_min",
        dest="rtt_min",
        type=int,
        help="Minimum round-trip time in tick units",
        required=True,
    )
    required.add_argument(
        "--ticks",
        dest="ticks",
        type=int,
        help="Number of ticks to run simulation for",
        required=True,
    )
    # optional arguments
    optional.add_argument(
        "--loss_ratio",
        dest="loss_ratio",
        type=float,
        help="independent and identically distributed loss probability, default 0",
        default=0.0,
    )
    optional.add_argument(
        "--queue_limit",
        dest="queue_limit",
        type=int,
        help="max. queue size of link queue, defaults to 1M packets, which is practically infinite",
        default=1000000,
    )
    optional.add_argument(
        "--window_size",
        dest="window_size",
        type=int,
        help="Window size in packets for sliding window sender",
    )
    optional.add_argument(
        "--min_timeout",
        dest="min_timeout",
        type=int,
        default=TimeoutCalculator.MIN_TIMEOUT,
        help="The minimum timeout value possible for the TimeoutCalculator",
    )
    optional.add_argument(
        "--max_timeout",
        dest="max_timeout",
        type=int,
        default=TimeoutCalculator.MAX_TIMEOUT,
        help="The minimum timeout value possible for the TimeoutCalculator",
    )
    parser._action_groups.append(optional)

    # Actually carry out parsing
    args = parser.parse_args()
    for arg in vars(args):
        print("%s: %s" % (arg, getattr(args, arg)))

    # Create the host based on the host_type, i.e., what protocol the host follows
    if args.host_type == "stopandwait":
        host = StopAndWaitHost(
            min_timeout=args.min_timeout, max_timeout=args.max_timeout
        )
    elif args.host_type == "slidingwindow":
        if args.window_size is None:
            raise argparse.ArgumentTypeError(
                "window_size must be defined for host_type SlidingWindow"
            )
        host = SlidingWindowHost(
            args.window_size,
            min_timeout=args.min_timeout,
            max_timeout=args.max_timeout,
        )
    elif args.host_type == "aimd":
        host = AimdHost(
            min_timeout=args.min_timeout, max_timeout=args.max_timeout
        )
    else:
        assert False

    simulator = Simulator(
        host, args.loss_ratio, args.queue_limit, args.rtt_min, args.seed
    )
    for tick in range(0, args.ticks):
        simulator.tick(tick)

    # Report the largest sequence number that has been received in order
    print(
        "Maximum in order received sequence number "
        + str(simulator.host.in_order_rx_seq)
    )
