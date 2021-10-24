#!/usr/bin/env python3
from simulator import Simulator
from sliding_window_host import SlidingWindowHost
# from starter_code.timeout_calculator import TimeoutCalculator
from timeout_calculator import TimeoutCalculator

def return_congested_simulator(host):
    # TODO: Create simulator that shows a congestion collapse setting.
    #what should be rtt min?
    simulator = Simulator(host, 0.0, 1000000, 10 ,1000)

    # Use  0.0 for loss_ratio, 1000 for the seed, and 1000000 for queue_limit.
    return simulator


def tick_and_get_seq_number(window):
    host = SlidingWindowHost(window, verbose=False)
    simulator = return_congested_simulator(host)
    for tick in range(0, 10000):
        simulator.tick(tick)
    # Return the largest sequence number that has been received in order
    print(
        "Maximum in order received sequence number "
        + str(simulator.host.in_order_rx_seq)
    )
    return simulator.host.in_order_rx_seq


def get_window_sizes():
    window_sizes = []
    return window_sizes


def main():
    # TODO: Select a progression of window sizes, which show a congestion collapse curve.

    #what does he mean by that?

    window_sizes = get_window_sizes(2, 5, 10, 20, 30, 50, 80, 100, 300, 500, 600 , 1000)    # Should have at least 10 entries.
    assert len(window_sizes) >= 10
    # Windows should be strictly increasing

    assert all(x <= y for x, y in zip(window_sizes, window_sizes[1:]))
    # TODO: For each window size, call tick_and_get_seq_number
    res = []
    for x in window_sizes:
        ordernum = tick_and_get_seq_number(x)
        res.append(ordernum)
        
        




    # TODO: Collect the results
    seq_numbers = []



    # Optional" Plot the results
    
    


if __name__ == "__main__":
    main()
