import sys
import matplotlib.pyplot as plt


class Ewma:
    def __init__(self, alpha):

        # number of rtt samples
        NUM_SAMPLES = 100

        # initialize all of them to zero
        rtt_samples = [0.0] * NUM_SAMPLES

        # rtt after being smoothed by EWMA
        self.smooth_rtt = [0.0] * NUM_SAMPLES

        # Create a pattern where the first half of the samples are 1
        for i in range(0, int(NUM_SAMPLES * 0.7)):
            rtt_samples[i] = 1.0

        # And the next half are 2
        for i in range(int(NUM_SAMPLES * 0.7), int(NUM_SAMPLES * 0.8)):
            rtt_samples[i] = 2.0

        # And the next half are 1
        for i in range(int(NUM_SAMPLES * 0.8), NUM_SAMPLES):
            rtt_samples[i] = 1.0

        # initialize mean rtt to 1
        mean_rtt = 1

        # convert the input to float
        alpha = float(alpha)

        # Iterate over all samples
        for i in range(0, NUM_SAMPLES):
            # TODO: Update mean rtt using EWMA equation
            #check later
            mean_rtt = (1-alpha)*mean_rtt + (alpha*rtt_samples[i])
            # Write it into the ith location of smooth_rtt
            self.smooth_rtt[i] = mean_rtt

    def plot(self):
        # plot the distribution
        plt.plot(self.smooth_rtt)
        plt.ylim([0, 2.5])
        plt.show()


def main(alpha):
    # If we use an argument, plot the argument only
    if alpha is not None:
        ewma = Ewma(alpha)
        print("EWMA at step 75")
        print("Alpha %s: RTT %s" % (alpha, ewma.smooth_rtt[75]))
        print("EWMA at step 90")
        print("Alpha %s: RTT %s" % (alpha, ewma.smooth_rtt[90]))
        ewma.plot()
        return
    # get alpha from the command line
    ewma1 = Ewma(1)
    ewma2 = Ewma(0.1)
    ewma3 = Ewma(0.05)
    ewma4 = Ewma(0.01)
    # ewma1.plot()
    # ewma2.plot()
    # ewma3.plot()
    # ewma4.plot()
    print("EWMA at step 75")
    print("Alpha 1: RTT %s" % ewma1.smooth_rtt[75])
    print("Alpha 0.1: RTT %s" % ewma2.smooth_rtt[75])
    print("Alpha 0.05: RTT %s" % ewma3.smooth_rtt[75])
    print("Alpha 0.01: RTT %s" % ewma4.smooth_rtt[75])
    print("EWMA at step 90")
    print("Alpha 1: RTT %s" % ewma1.smooth_rtt[90])
    print("Alpha 0.1: RTT %s" % ewma2.smooth_rtt[90])
    print("Alpha 0.05: RTT %s" % ewma3.smooth_rtt[90])
    print("Alpha 0.01: RTT %s" % ewma4.smooth_rtt[90])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        alpha_arg = None
    else:
        alpha_arg = float(sys.argv[1])
    main(alpha_arg)
