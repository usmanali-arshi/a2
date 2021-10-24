from packet import Packet
from timeout_calculator import TimeoutCalculator

# Structure to store information associated with an unacked packet
# so that we can maintain a list of such UnackedPacket objects


class AimdHost:
    """
    This class implements a host that follows the AIMD protocol.
    Data members of this class are

    **unacked**: List of unacked packets

    **window**: Size of the window at any given moment

    **max_seq**: Maximum sequence number sent so far

    **in_order_rx_seq**: Maximum sequence number received so far

    **slow_start**: Boolean to indicate whether algorithm is in slow start or not

    **next_decrease**: Time (in ticks) at which the window size should be decreased

    **timeout_calculator**: An object of class TimeoutCalculator
    (Refer to TimeoutCalculator class for more information)

    There are two member functions - send and recv that perform the task of sending
    and receiving packets respectively. All send and receive logic should be written
    within one of these two functions.

    """

    def __init__(
        self,
        verbose=True,
        min_timeout=TimeoutCalculator.MIN_TIMEOUT,
        max_timeout=TimeoutCalculator.MAX_TIMEOUT,
    ):
        # list of unacked packets
        self.unacked = []
        self.window = 1
        # We'll initialize window to 1
        self.max_seq = -1
        # maximum sequence number sent so far
        self.in_order_rx_seq = -1
        # maximum sequence number received so far in order
        # Are we in slow start?
        self.slow_start = True
        # When to next decrease your window; adds some hystersis
        self.next_decrease = -1
        # Whether to print output
        self.verbose = verbose
        # object for computing timeouts
        self.timeout_calculator = TimeoutCalculator(
            verbose=verbose, min_timeout=min_timeout, max_timeout=max_timeout
        )

    def send(self, tick):
        """
        Function to send packet on to the network. Host should first retransmit
         any unacked packets that have timed out.
         Host should also decrease the window size if it is time for the next
         decrease. After attempting retransmissions, if the window is not full,
         fill up the window with new packets.

        Args:

            **tick**: Simulated time

        Returns:

            A list of packets that the host wants to transmit on to the network
        """
        if self.verbose:
            print("@ tick " + str(tick) + " window is " + str(self.window))

        # TODO: Create an empty list of packets that the host will send
        pkts = []
        # First, process retransmissions
        for i in range(0, len(self.unacked)):
            unacked_pkt = self.unacked[i]
            if tick >= unacked_pkt.timeout_tick:
                if self.verbose:
                    print(
                        "@ "
                        + str(tick)
                        + " timeout for unacked_pkt "
                        + str(unacked_pkt.seq_num)
                        + " timeout duration was "
                        + str(unacked_pkt.timeout_duration)
                    )
                # TODO: Retransmit any packet that has timed out

                # by doing the following in order
                # (1) creating a new packet,
                pkt = Packet(tick , unacked_pkt.seq_num)
                # (2) Incrementing num_retx (for debugging purposes)
                pkt.num_retx +=1
                # (3) Append the packet to the list of packets created earlier
                pkts.append(pkt)
                # (4) Backing off the timer
                self.timeout_calculator.exp_backoff () 
                # (5) Updating timeout_tick and timeout_duration appropriately after backing off the timer
                # unacked_pkt.timeout_tick = self.timeout_calculator.update_timeout(tick)
                pkt.timeout_duration = tick - unacked_pkt.timeout_tick #not sure at all
                pkt.timeout_tick =  tick + pkt.timeout_duration
                
                if self.verbose:
                    print(
                        "@ "
                        + str(tick)
                        + " exp backoff for packet "
                        + str(unacked_pkt.seq_num)
                    )
                # TODO: Multiplicative decrease, if it's time for the next decrease
                if (tick == self.next_decrease):
                    # Cut window by half, but don't let it go below 1
                    self.window /=2
                    if self.window < 1:
                        self.window =1
                    # TODO: Make sure the next multiplicative decrease doesn't happen until an RTT later
                    self.next_decrease = tick + self.timeout_calculator.mean_rtt
                
                # (use the timeout_calculator to estimate the RTT)


                # Exit slow start, whether you were in it or not
                self.slow_start = False

            self.unacked[i] = unacked_pkt

        # Now fill up the window with new packets
        while len(self.unacked) < self.window:
            # TODO: Replace this break


            #break
            # TODO: Create new packets, set their retransmission timeout, and transmit them
            new_pkt = Packet (tick, self.max_seq+1)
            new_pkt.timeout_tick = self.timeout_calculator.timeout + tick


            # TODO: Remember to update self.max_seq and add the just sent packet to self.unacked
            self.max_seq = new_pkt.seq_num
            self.unacked.append(new_pkt)

        # TODO: Return the list of packets that need to be sent on to the network
        return pkts

    def recv(self, pkt, tick):
        """
        Function to get a packet from the network.

        Args:

            **pkt**: Packet received from the network

            **tick**: Simulated time
        """
        assert tick > pkt.sent_ts
        #pass
        # TODO: Compute RTT sample
        rtt_sample = tick - pkt.sent_ts
        # TODO: Update timeout
        self.timeout_calculator.update_timeout(rtt_sample)



        # TODO: Remove received packet from self.unacked
        for i in range(0, len(self.unacked)):
            unacked_pkt = self.unacked[i]
            if unacked_pkt.seq_num == pkt.seq_num:
                self.unacked.pop(i)

        # TODO: Update in_order_rx_seq to reflect the largest sequence number that you
        # have received in order so far
        
        #or 
        # self.in_order_rx_seq = pkt.seq_num
        if pkt.seq_num == self.in_order_rx_seq +1:
            self.in_order_rx_seq +=1

        # TODO: Increase your window given that you just received an ACK. Remember that:
        # 1. The window increase rule is different for slow start and congestion avoidance.
        if (self.slow_start):
            self.window +=1
        #congestion control
        else:
            self.window += (1/self.window)


        # 2. The recv() function is called on every ACK (not every RTT), so you should adjust your window accordingly.
