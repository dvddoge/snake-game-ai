# Snake Game AI with Reinforcement Learning

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project implements an AI agent that learns to play the classic Snake game using reinforcement learning techniques. The AI uses a Q-learning algorithm with a neural network (Deep Q-Network) to make decisions and improve its performance over time.

The game is built using Pygame, and the AI agent is implemented using PyTorch for the neural network and training process.

## Features

- Classic Snake game implementation with Pygame
- Reinforcement learning AI agent using Deep Q-Network
- Visualization of the game and learning progress
- Customizable game parameters and learning hyperparameters

## Requirements

- Python 3.7+
- PyTorch
- Pygame
- Matplotlib (for plotting learning progress)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/snake-game-ai.git
   cd snake-game-ai
   ```

2. Install the required packages:
   ```
   pip install torch pygame matplotlib
   ```

## How to Run

To start the training process:

```
python agent.py
```

This will launch the game window and begin the AI training process. You'll see the snake moving and learning to play the game over time.

## Project Structure

- `snakegame.py`: Contains the `SnakeGameAI` class, which implements the game logic and rendering.
- `model.py`: Defines the `Linear_QNet` (neural network) and `QTrainer` classes for the AI agent.
- `agent.py`: Implements the `Agent` class and the main training loop.
- `helper.py`: Contains utility functions, including the plotting function for visualizing progress.

## How It Works

1. **Game State**: The game state is represented as a set of 11 boolean values, indicating danger straight, right, and left, the current direction, and the food location relative to the snake's head.

2. **Neural Network**: A simple feedforward neural network with one hidden layer processes the game state and outputs Q-values for three possible actions: straight, right turn, or left turn.

3. **Q-Learning**: The agent uses an ε-greedy policy for exploration and exploitation. It stores experiences in a replay memory and periodically trains the neural network using random batches from this memory.

4. **Training Process**: The agent plays multiple games, continuously learning from its experiences. The neural network is updated to minimize the difference between predicted Q-values and target Q-values calculated using the Bellman equation.

5. **Visualization**: The game is rendered using Pygame, allowing you to watch the AI's progress in real-time. A plot of scores over time is also generated to track improvement.

## Customization

You can customize various aspects of the game and learning process:

- In `snakegame.py`: Modify `dis_width`, `dis_height`, `snake_speed`, etc., to change game parameters.
- In `agent.py`: Adjust `MEMORY`, `BATCH_SIZE`, `LR`, etc., to fine-tune the learning process.
- In `model.py`: Modify the neural network architecture by changing the `Linear_QNet` class.

## Contributing

Contributions to this project are welcome! Here are some ways you can contribute:

- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or new functionalities

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy watching the AI learn to play Snake, and feel free to experiment with the code to improve its performance!
