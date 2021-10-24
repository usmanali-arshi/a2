class TimeoutCalculator:
    # default values for minimum and maximum timeout
    MIN_TIMEOUT = 100
    MAX_TIMEOUT = 10000
    """
    Timeout Calculator maintains the mean RTT and RTT variance.
    Data members of this class include alpha, beta and K
     (which have the same meaning as discussed in the lectures)
    """

    def __init__(self, min_timeout, max_timeout, verbose=True):
        # minimum possible timeout
        self.min_timeout = min_timeout
        # maximum possible timeout
        self.max_timeout = max_timeout
        self.mean_rtt = 0.0
        self.rtt_var = 0.0
        # alpha value taken from TCP's retransmission timer
        self.alpha = 0.125
        # beta value taken from TCP's retransmission timer
        self.beta = 0.25
        # what multiple of RTT variation to use in the timeout
        self.k = 4.0
        # Initialize timeout to the minimum possible value
        self.timeout = min_timeout
        # EWMA is not initialized until the first sample is seen
        self.ewma_init = False
        # Whether to print output
        self.verbose = verbose

    def update_timeout(self, rtt_sample):
        """
        This function is used to update the mean and variance RTTs
        """
        # If you have seen no RTTs yet or exponentially backed off before
        if not self.ewma_init:
            pass
            # TODO: Initialize mean_rtt to current sample
            self.mean_rtt = rtt_sample
            # TODO: Initialize rtt_var to half of curent sample
            self.rtt_var = rtt_sample/2
            # TODO: Set timeout using mean_rtt and rtt_var
            self.timeout = self.mean_rtt + (self.k*self.rtt_var)

            # TODO: Remember to update self.ewma_init correctly so that the else branch is taken on subsequent packets.
            self.ewma_init = True
        else:
            pass
            # TODO: Update RTT var based on rtt_sample and old mean RTT
            self.rtt_var = (1-self.beta)*self.rtt_var + self.beta* (rtt_sample - self.mean_rtt)

            # TODO: Update mean RTT based on rtt_sample
            self.mean_rtt = (1- self.alpha)* self.mean_rtt + self.alpha* rtt_sample
            # TODO: Update timeout based on mean RTT and RTT var
            self.timeout = self.mean_rtt + (self.k*self.rtt_var)

        # TODO: Before you return from this function,
        # ensure that updated timeout is between self.min_timeout and self.max_timeout
        if self.timeout > self.max_timeout:
            self.timeout = self.max_timeout
        if self.timeout < self.min_timeout:
            self.timeout = self.min_timeout
        
        # i.e, if your timeout is above self.max_timeout, you should set it to self.max_timeout.
        # and  if it's below self.min_timeout, you should set it to self.min_timeout

    def exp_backoff(self):
        """
        This function is used to double the timeout representing an exponential backoff
        """
        pass
        # TODO: Exponentially back off by doubling the timeout
        self.timeout = self.timeout* 2
        # TODO: Re-initialize the EWMA
 

        self.ewma_init= False
        print("exponential backoff here, re-initializing EWMA")
        # TODO: Before you return from this function,
        # ensure that updated timeout is between self.min_timeout and self.max_timeout
        # i.e, if your timeout is above self.max_timeout, you should set it to self.max_timeout.
        # and  if it's below self.min_timeout, you should set it to self.min_timeout
        if self.timeout > self.max_timeout:
            self.timeout = self.max_timeout
        if self.timeout < self.min_timeout:
            self.timeout = self.min_timeout
        
        
        return self.timeout


def main():
    # This is a simple example for you to experiment. This is not part of the
    # submission
    timeout = TimeoutCalculator(
        TimeoutCalculator.MIN_TIMEOUT, TimeoutCalculator.MAX_TIMEOUT
    )
    print(timeout.exp_backoff())


if __name__ == "__main__":
    main()
