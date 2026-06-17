import random
import statistics

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

class Environment:
    def __init__(self, reward_map, transition_noise=0.0):
        self.reward_map = reward_map
        self.transition_noise = transition_noise

    def step(self, state, action):
        next_state = self._next_state(state, action)
        reward = self.reward_map.get(next_state, 0)
        return next_state, reward

    def _next_state(self, state, action):
        if random.random() < self.transition_noise:
            return random.choice(list(self.reward_map.keys()))

        if action == 'a':
            return min(state + 1, max(self.reward_map.keys()))
        if action == 'b':
            return max(state - 1, min(self.reward_map.keys()))
        return state

class Model:
    def __init__(self, env, accuracy):
        self.env = env
        self.accuracy = accuracy

    def predict(self, state, action):
        if random.random() > self.accuracy:
            # erreur de prédiction : transition aléatoire
            return random.choice(list(self.env.reward_map.keys()))
        return self.env._next_state(state, action)

class Agent:
    def __init__(self, model):
        self.model = model

    def choose_action(self, state):
        pred_a = self.model.predict(state, 'a')
        pred_b = self.model.predict(state, 'b')
        reward_a = self.model.env.reward_map.get(pred_a, 0)
        reward_b = self.model.env.reward_map.get(pred_b, 0)
        return 'a' if reward_a >= reward_b else 'b'

    def run_episode(self, env, start_state, steps=10):
        state = start_state
        total_reward = 0
        for _ in range(steps):
            action = self.choose_action(state)
            state, reward = env.step(state, action)
            total_reward += reward
        return total_reward


def evaluate_model_accuracy(accuracy, trials=100, steps=10):
    reward_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    env = Environment(reward_map, transition_noise=0.1)
    model = Model(env, accuracy)
    agent = Agent(model)

    rewards = [agent.run_episode(env, start_state=0, steps=steps) for _ in range(trials)]
    return statistics.mean(rewards), statistics.stdev(rewards)


def main():
    accuracies = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    print('Accuracy | Mean reward | Std dev')
    print('--------|-------------|---------')
    results = []
    print('Accuracy | Mean reward | Std dev')
    print('--------|-------------|---------')
    for acc in accuracies:
        mean_reward, std_reward = evaluate_model_accuracy(acc)
        results.append((acc, mean_reward, std_reward))
        print(f'{acc:0.1f}      | {mean_reward:0.2f}       | {std_reward:0.2f}')

    if plt is None:
        print('\nmatplotlib n\'est pas installé. Installez-le avec `pip install matplotlib` pour afficher le graphique.')
        return

    accuracies_plot = [r[0] for r in results]
    mean_rewards = [r[1] for r in results]
    plt.figure(figsize=(8, 5))
    plt.plot(accuracies_plot, mean_rewards, marker='o', linestyle='-')
    plt.title('Influence de la précision du modèle sur la fiabilité de l\'agent')
    plt.xlabel('Précision du modèle')
    plt.ylabel('Récompense moyenne')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

