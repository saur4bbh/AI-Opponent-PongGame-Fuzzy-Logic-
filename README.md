🏓 Pong Game AI Opponent using Fuzzy Logic (Mamdani & TSK)

📌 Overview

This project implements an intelligent AI opponent for the classic Pong game using Fuzzy Logic Control Systems. The AI paddle movement is controlled using two different fuzzy inference approaches:

Mamdani Fuzzy Inference System
Takagi–Sugeno–Kang (TSK) Fuzzy Model

The objective is to demonstrate how fuzzy logic can be applied to real-time decision-making in dynamic game environments and simulate human-like reasoning under uncertainty.

🧠 Fuzzy Logic Approach

1️⃣ Mamdani Model

Uses linguistic variables (e.g., Near, Far, Fast, Slow).
Based on IF–THEN fuzzy rules.
Applies fuzzification → rule evaluation → aggregation → defuzzification.
Produces smooth and interpretable paddle movement.

Example Rule:
IF Ball_Distance is Near AND Ball_Speed is Fast  
THEN Paddle_Move is Up

2️⃣ Takagi–Sugeno–Kang (TSK) Model

Uses fuzzy inputs but mathematical functions as outputs.
Outputs are weighted linear functions.
Faster computation compared to Mamdani.
More suitable for real-time systems.

Example Rule:
IF Ball_Distance is Near AND Ball_Speed is Fast  
THEN Paddle_Move = a*(Distance) + b*(Speed) + c

🕹 Gameplay Logic

The game continuously tracks ball position and velocity every frame.
Inputs (Ball's position and Paddle's position) are fed into the fuzzy controller.
Fuzzy inference is performed (Mamdani or TSK).
A crisp output is generated (AI Paddle's direction and speed)
The paddle moves accordingly.

🚀 How to Run

Clone the repository:
git clone https://github.com/your-username/your-repo-name.git

Navigate into the project directory:
cd your-repo-name

Run the main file:
python main.py (make sure requirement libraries installment is satisfied)

🔮 Future Improvements

Adaptive rule tuning
Neuro-fuzzy (ANFIS) integration
Performance benchmarking metrics
