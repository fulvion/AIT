import numpy as np

class Bayes:
    def __init__(self, hypos, priors, obs, likelihood):
        self.hypothesis = hypos #["Bowl1", "Bowl2"] STATE 
        self.priors = priors #[0.5, 0.5]
        self.obs = obs #["chocolate", "vanilla"] OBSERVATION
        self.likelihoods = likelihood #[[15/50, 35/50], [30/50, 20/50]]

    def likelihood(self, observation, hypothesis):
        return (self.likelihoods[self.hypothesis.index(hypothesis)][self.obs.index(observation)])

    def norm_constant(self, observation):
        temp = 0
        for hypo in self.hypothesis:
            hypoIndex = self.hypothesis.index(hypo)
            temp = temp + (self.priors[hypoIndex] * self.likelihoods[hypoIndex][self.obs.index(observation)])
        return round(temp, 3)
    
    def single_posterior_update(self, observation, prior):
        posterior = []
        for hypo in self.hypothesis:
            hypoIndex = self.hypothesis.index(hypo)
            prior = self.priors[hypoIndex]
            likelihood = self.likelihood(observation, hypo)
            evidence = self.norm_constant(observation)
            posterior.append((prior * likelihood) / evidence)
        return list(map(lambda x: round(x, 3), posterior))
    
    
    def compute_posterior(self, observations):
        posterior = [1 for i in range(len(self.hypothesis))]
        for o in observations:
            current_p = self.single_posterior_update(o, self.priors)
            posterior = np.multiply(posterior, current_p)
        return posterior

if __name__ == '__main__':
    hypos = ["Bowl1", "Bowl2"]
    priors = [0.5, 0.5]
    obs = ["chocolate", "vanilla"]
    # e.g. likelihood[0][1] corresponds to the likehood of Bowl1 and vanilla, or 35/50
    likelihood = [[15/50, 35/50], [30/50, 20/50]]

    b = Bayes(hypos, priors, obs, likelihood)

    with open("group_40.txt", "w") as text_file:
        l = b.likelihood("vanilla", "Bowl1")
        print("likelihood(vanilla, Bowl1) = %s " % l)
        text_file.write("likelihood(vanilla, Bowl1) = %s \n" % l)

        n_c = b.norm_constant("vanilla")
        print("normalizing constant for vanilla: %s" % n_c)
        text_file.write("normalizing constant for vanilla: %s\n" % n_c)

        p_1 = b.single_posterior_update("vanilla", [0.5, 0.5])
        print("vanilla - posterior: %s" % p_1)
        text_file.write("vanilla - posterior: %s\n" % p_1)

        p_2 = b.compute_posterior(["chocolate", "vanilla"])
        print("chocolate, vanilla - posterior: %s" % p_2)
        text_file.write("chocolate, vanilla - posterior: %s\n" % p_2)

        text_file.close()
        