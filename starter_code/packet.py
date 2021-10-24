class Packet:
    """
    Class to represent a simulated packet. It has the following data members

    **sent_ts**: Time at which the packet was sent

    **seq_num**: Sequence number of the packet

    **pdbox_time**: Arrival time at the propogation delay box

    **retx**: To identify if the packet is a retransmission

    """

    def __init__(self, sent_ts, seq_num):
        self.sent_ts = sent_ts  # sent timestamp, used to compute RTTs
        self.seq_num = seq_num  # sequence number, starting from 0
        self.pdbox_time = -1  # arrival time at prop delay box
        self.num_retx = 0  # how many times it's been retransmitted so far
        self.timeout_duration = 0  # what is the duration of its timeout
        self.timeout_tick = 0  # at what tick does this packet timeout?

    def __repr__(self):
        # Debugging: printing a packet object displays its sequence number
        return str(self.seq_num)
