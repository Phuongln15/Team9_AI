import random
import gym


def spawnIndividual(length):
    geneticCode = random.choices([0, 1, 2, 3, 4, 5], k=length)
    return geneticCode


class Population:

    def __init__(self, popSize, pathLength):
        if popSize > 0 and pathLength > 0:
            self.fitnesses = []
            self.individuals = []
            for i in range(popSize):
                self.individuals.append(spawnIndividual(pathLength))
        else:
            print("WRONG!! both inputs of population size and action sequcence length must be positive")

    def checkPathFitness(self, env):
        for indv in self.individuals:
            personalFitness = 0
            env.reset()
            for action in indv:
                observation, reward, done, ignore = env.step(action)
                personalFitness += reward
                if done:
                    personalFitness += 90
                    break
                elif list(env.decode(observation))[2] == 4:
                    # pass
                    personalFitness += 1
            self.fitnesses.append(personalFitness)

    def checkPolicyFitness(self, env):
        if len(self.individuals[0]) >= 500:
            for indv in self.individuals:
                personalFitness = 0
                observation = env.reset()

                for i in range(500):
                    observation, reward, done, ignore = env.step(indv[observation])
                    personalFitness += reward
                    if done:
                        break

                self.fitnesses.append(personalFitness)
        else:
            print("wrong! an individual needs a length of at least 500, but anything past 500 is ignored")

    def evolve(self, env, popType, generations=200, surviveBySkill=0.25, surviveByChance=0.05, mutationRate=0.05):

        # evaluate the population
        self.fitnesses = []
        if popType == 'path':
            self.checkPathFitness(env)
        elif popType == 'policy':
            self.checkPolicyFitness(env)
        else:
            raise ValueError(popType, " type of population does not exist")

        aveFit = [sum(self.fitnesses) / len(self.fitnesses)]
        fitest = ([], -9999999)
        i = 0
        while i < generations:
            scores = zip(self.fitnesses, self.individuals)
            scores = sorted(scores, reverse=True)
            sortedIndvs = [x[1] for x in scores]

            if scores[0][0] > fitest[1]:
                fitest = (scores[0][1], scores[0][0])

            # trim the heard
            skilled = sortedIndvs[:int(len(sortedIndvs) * surviveBySkill)]
            lucky = random.sample(sortedIndvs[int(len(sortedIndvs) * surviveBySkill):],
                                  k=int(len(sortedIndvs) * surviveByChance))
            parents = skilled + lucky

            # breed em and weep
            children = []
            while len(children) < len(self.individuals) - len(parents):
                par1 = parents[random.randint(0, len(parents) - 1)]
                par2 = parents[random.randint(0, len(parents) - 1)]
                if par1 != par2:
                    split = int(len(par1) / 2)
                    children.append(par1[:split] + par2[split:])
            self.individuals = parents + children

            # mutate the survivors
            mutated = random.sample(range(len(self.individuals)), k=int(len(sortedIndvs) * mutationRate))
            for index in mutated:
                self.individuals[index][random.randint(0, len(self.individuals[index]) - 1)] = random.randint(0, 5)

            self.fitnesses = []
            if popType == 'path':
                self.checkPathFitness(env)
            elif popType == 'policy':
                self.checkPolicyFitness(env)

            aveFit.append(sum(self.fitnesses) / len(self.fitnesses))

            i += 1

        return fitest[0], aveFit


if __name__ == "__main__":
    # Evolve a path
    pop = Population(200, 100)
    environ = gym.make('Taxi-v3').env

    best_path, path_fitness_curve = pop.evolve(environ, 'path', 100)
    print("path evolution\n")

    environ.reset()
    for action in best_path:
        environ.render()
        _, __, done, ___ = environ.step(action)
        if done:
            break
    environ.close()
    print("\n", path_fitness_curve)

    # Evolve a policy
    pop = Population(300, 500)
    environ = gym.make('Taxi-v3').env

    best_policy, policy_fitness_curve = pop.evolve(environ, 'policy', 10000)
    print("\npolicy evolution\n")

    observation = environ.reset()
    for i in range(500):
        environ.render()
        observation, _, done, __ = environ.step(best_policy[observation])
        if done:
            break
    environ.close()
    print("\n", best_policy, "\n", policy_fitness_curve)
