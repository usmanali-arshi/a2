from packet import Packet
from timeout_calculator import TimeoutCalculator


class StopAndWaitHost:
    """
    This host implements the stop and wait protocol. Here the host only
    sends one packet in return of an acknowledgement.
    """

    def __init__(
        self,
        verbose=True,
        min_timeout=TimeoutCalculator.MIN_TIMEOUT,
        max_timeout=TimeoutCalculator.MAX_TIMEOUT,
    ):
        # maximum sequence number received so far in order
        self.in_order_rx_seq = -1
        # can we send a packet or are we still waiting for an ACK?
        self.ready_to_send = True
        # when was this packet sent out last?
        self.packet_sent_time = -1
        # initialize TimeoutCalculator
        self.timeout_calculator = TimeoutCalculator(
            verbose=verbose, min_timeout=min_timeout, max_timeout=max_timeout
        )
        # Whether to print output
        self.verbose = verbose

    def send(self, tick):
        """
        Function to send a packet with the next sequence number on to the network.
        """
        if self.ready_to_send:
            # TODO: Send next sequence number by creating a packet
            #check before submitting pls
            pkt = Packet(tick, self.in_order_rx_seq +1)

            # TODO: Remember to update packet_sent_time and ready_to_send appropriately
            self.packet_sent_time = tick
            self.ready_to_send = False

            # TODO: Return the packet
            if self.verbose:
                print(
                    "sent packet @ "
                    + str(tick)
                    + " with sequence number "
                    + str(pkt.seq_num)
                )
            return pkt
        elif tick - self.packet_sent_time >= self.timeout_calculator.timeout:
            pass
            # TODO: Timeout has been exceeded, retransmit packet
            #check pls
            pkt = Packet(tick, self.in_order_rx_seq +1)
            self.packet_sent_time = tick


            # following the same procedure as above when transmitting a packet for the first time
            
            # TODO: Exponentially back off the timer
            
            self.timeout_calculator.exp_backoff()

            # TODO: Increment num_retx field on packet to detect retransmissions for debugging
            pkt.num_retx +=1
            # TODO: Return the packet
            # return pkt
            if self.verbose:
                print(
                    "retx packet @ "
                    + str(tick)
                    + " with sequence number "
                    + str(pkt.seq_num)
                )
            return pkt
        # If we do not time out and are not ready to send, do nothing.
        #check we have to do somethign here?

    def recv(self, pkt, tick):
        """
        Function to get a packet from the network.

        Args:

            **pkt**: Packet received from the network

            **tick**: Simulated time
        """
        assert tick > pkt.sent_ts
        pass
        if self.verbose:
            print(
                "@ "
                + str(tick)
                + " timeout computed to be "
                + str(self.timeout_calculator.timeout)
            )
        # TODO: Compute RTT sample
        #check 
        rtt_sample = tick - pkt.sent_ts
        

        # TODO: Update timeout based on RTT sample
        #check
        self.timeout_calculator.update_timeout(rtt_sample)

        # TODO: Update self.in_order_rx_seq and self.ready_to_send depending on pkt.seq_num
        #check pls
        if (pkt.seq_num == (self.in_order_rx_seq+1)):
            self.in_order_rx_seq = pkt.seq_num
            self.ready_to_send = True
        else:
            self.ready_to_send = False


        # TODO: Only print this when you received the packet
        if pkt.seq_num == (self.in_order_rx_seq+1):

            if self.verbose:
                print(
                    "rx packet @ "
                    + str(tick)
                    + " with sequence number "
                    + str(pkt.seq_num)
                )
