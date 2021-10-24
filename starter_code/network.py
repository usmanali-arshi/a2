# Required for dropping packets at random
import queue
import random


class DelayBox:
    """
    A class to delay packets by the propagation delay
    In our case, we'll use it to delay packets by the two-way propagation delay,
    i.e., RTT_min
    """

    def __init__(self, prop_delay):
        # queue of packets being delayed
        self.prop_delay_queue = []
        # how much to delay them by
        self.prop_delay = prop_delay

    def recv(self, pkt, tick):
        # enqueue packet after timestamping it
        pkt.pdbox_time = tick
        self.prop_delay_queue += [pkt]

    def tick(self, tick, host):
        # execute this on every tick
        # packets that are delivered this tick
        to_deliver = []
        for pkt in self.prop_delay_queue:
            # if propagation delay has been exceeded
            if pkt.pdbox_time + self.prop_delay <= tick:
                assert pkt.pdbox_time + self.prop_delay == tick
                to_deliver += [pkt]
                # deliver to the host
                host.recv(pkt, tick)
        self.prop_delay_queue = [
            x for x in self.prop_delay_queue if x not in to_deliver
        ]


class Link:
    """
    A class to represent a link with a finite capacity of 1 packet per tick
    We can generalize this to other capacities, but we're keeping the assignment simple
    """

    def __init__(self, loss_ratio, queue_limit, verbose=True):
        # queue of packets at the link
        self.link_queue = queue.Queue()
        # probability of dropping packets when link dequeues them
        self.loss_ratio = loss_ratio
        # Max size of queue in packets
        self.queue_limit = queue_limit
        # Whether to print statements
        self.verbose = verbose

    def recv(self, pkt):
        """
        Function to receive a packet from a device connected at either
        ends of the link. Device here can represent an end host or any other
        network device.

        The device connected to the link needs to call the recv function to put
        packet on to the link. If link's queue is full, it starts dropping packets
        and does not receive any more packets.
        """
        if self.link_queue.qsize() < self.queue_limit:
            self.link_queue.put(pkt)  # append to the queue
        else:
            if self.verbose:
                print("Link dropped packet because queue_limit was exceeded")

    def tick(self, tick, pdbox):
        # Execute on every tick
        """
        This function simulates what a link would do at each time instant (tick).
        It dequeue packets and sends it to the propagation delay box
        """
        # Dequeue from link queue if queue is not empty
        if self.link_queue.qsize() != 0:
            head = self.link_queue.get()
            if random.uniform(0.0, 1) < (1 - self.loss_ratio):
                # dequeue and send to prop delay box
                pdbox.recv(head, tick)
            else:
                if self.verbose:
                    print("@ tick ", tick, " link dropped a packet ")
