<!-- ABOUT THE PROJECT -->
## About The Project
Reinforcement Learning agent which learns to play a game

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Windows 11
python == ^3.10.2
pip == ^22.3.1
CUDA == 12.0.0

### Installation

This part describes the installation for windows 11.

1. open the git bash in project folder
2. install virtualenv with pip
   ```
   pip install virtualenv
   ```
3. create a virtual enviremont
   ```
   virtualenv .venv
   ```
4. activate your virtual enviremont
   ```
   source .venv/Scripts/activate
   ```
5. install the needed packages
   ```
   pip install -r requirements.txt
   ```
<!-- USAGE EXAMPLES -->
## Usage
1. start the gym_game/main.py
   ```
   python gym_game/main.py
   ```
2. the game will start and simulate a keyboard to interact with the game,
   dont interact with the keyboard to ensure not to disturb the training.
3. The training data is saved in model.pth
4. The taken actions are saved in action.txt

5. To only play the game without training start gym_game/GymCustomEnv/pythongame/SuperBros.py
   ```
   python gym_game/GymCustomEnv/pythongame/SuperBros.py
   ```