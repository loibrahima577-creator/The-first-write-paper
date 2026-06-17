import random
import statistics

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

class DeliveryEnvironment:
    def __init__(self, block_at_step=1, route_b_success=0.9):
        self.block_at_step = block_at_step
        self.route_b_success = route_b_success
        self.reset()

    def reset(self):
        self.step_count = 0
        self.route_a_open = True
        self.at_blocked_point = False

    def step(self, action):
        self.step_count += 1
        if self.step_count > self.block_at_step:
            self.route_a_open = False

        if action == 'A':
            if self.route_a_open:
                return 'goal', True
            return 'blocked', False

        if action == 'B':
            return ('goal', True) if random.random() < self.route_b_success else ('failure', False)

        return 'failure', False

class EnvironmentModel:
    def __init__(self):
        self.route_a_open = True

    def update(self, observation):
        if observation == 'blocked':
            self.route_a_open = False

class BaselineAgent:
    def __init__(self, model):
        self.model = model

    def choose_action(self):
        return 'A' if self.model.route_a_open else 'B'

    def observe(self, observation):
        # pas de mise à jour du modèle dans le baseline
        return

class LearningAgent(BaselineAgent):
    def observe(self, observation):
        self.model.update(observation)


def run_trial(agent_class, trials=100):
    env = DeliveryEnvironment(block_at_step=1, route_b_success=0.9)
    successes = []

    for _ in range(trials):
        env.reset()
        model = EnvironmentModel()
        agent = agent_class(model)

        # Première action : le plan initial est Route A.
        action = agent.choose_action()
        observation, success = env.step(action)

        if success and observation == 'goal':
            successes.append(True)
            continue

        # Si Route A est bloquée, le learning agent peut adapter son plan.
        agent.observe(observation)
        action = agent.choose_action()
        observation, success = env.step(action)
        successes.append(success)

    return statistics.mean(successes), statistics.stdev(successes)


def main():
    trials = 200
    baseline_rate, baseline_std = run_trial(BaselineAgent, trials=trials)
    learning_rate, learning_std = run_trial(LearningAgent, trials=trials)

    print('Agent                   | Recovery Rate | Std dev')
    print('------------------------|---------------|---------')
    print(f'Baseline (no learning)  | {baseline_rate:.2%}         | {baseline_std:.2f}')
    print(f'Environment learning    | {learning_rate:.2%}         | {learning_std:.2f}')

    if plt is None:
        print('\nmatplotlib n\'est pas installé. Installez-le avec `pip install matplotlib` pour afficher le graphique.')
        return

    labels = ['Baseline', 'Environment learning']
    rates = [baseline_rate * 100, learning_rate * 100]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, rates, color=['#d62828', '#2a9d8f'])
    plt.title('Recovery Rate après perturbation')
    plt.ylabel('Recovery Rate (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{rate:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    print('\nInterprétation :')
    print('- L\'agent baseline ne récupère pas après la perturbation.')
    print('- L\'agent avec apprentissage de l\'environnement s\'adapte et choisit un nouveau chemin.')

if __name__ == '__main__':
    main()
