# PathFinder
find the path uniformed search

AI Pathfinder - README

Yeh ek AI project hai jo 6 different search algorithms use karta hai grid mein rasta dhundhne ke liye. Start point se target tak ka shortest route find karta hai with visualization.

Features:

✅ 6 search algorithms (BFS, DFS, UCS, DLS, IDDFS, Bidirectional)

✅ 8-direction movement (including diagonals)

✅ Dynamic obstacles (randomly appear during execution)

✅ Real-time GUI visualization

✅ Step-by-step animation

📋 Requirements
Python 3.7 or higher

pip (Python package installer)

Internet connection for first-time setup

🚀 Quick Start - 2 Minute Mein Chalao
Step 1: Python Check Karo
bash
python --version
Agar error aye toh python.org se download karo

Step 2: Files Download Karo
Project folder mein yeh files hain:

text
pathfinder.py
requirements.txt
README.md
Step 3: Dependencies Install Karo
bash
pip install -r requirements.txt
Yeh command matplotlib aur numpy install karega

Step 4: Program Chalao
bash
python pathfinder.py
📦 Dependencies (Jo Install Hongi)
txt
# requirements.txt
matplotlib>=3.5.0
numpy>=1.21.0
Manual install bhi kar sakte ho:

bash
pip install matplotlib numpy
🎮 How to Use - Kaise Use Karo
Jab Program Chale Ga:
Grid dikhega - 10x10 ka grid

Colors ka matlab:

🔵 Blue = Start point

🟢 Green = Target

⚫ Black = Walls/Obstacles

🟡 Yellow = Frontier (next check hoga)

🔷 Light Blue = Explored (check ho chuka)

🔴 Red = Final path (mil gaya rasta!)

🟠 Orange = Dynamic obstacles (achanak auqaat)

Menu Options:
Program run karne par yeh menu dikhega:

text
=== AI Pathfinder ===
1. BFS (Breadth-First Search)
2. DFS (Depth-First Search)  
3. UCS (Uniform Cost Search)
4. DLS (Depth-Limited Search)
5. IDDFS (Iterative Deepening DFS)
6. Bidirectional Search
7. Dynamic Obstacles Demo
8. Exit
Enter choice (1-8):
Bas number enter karo aur dekhlo magic! ✨

🔧 Common Issues - Maslay Aur Hal
Masla 1: "No module named matplotlib"
Hal:

bash
pip install matplotlib numpy
Masla 2: GUI window nahi khulti
Windows pe:

bash
python -m pip install --upgrade pip
python -m pip install matplotlib numpy
Mac pe:

bash
brew install python-tk
pip install matplotlib numpy
Linux pe:

bash
sudo apt-get install python3-tk
pip3 install matplotlib numpy
Masla 3: Animation bht fast hai
Hal: pathfinder.py mein yeh line dhoondo:

python
viz.animate(delay=100)  # 100 ko 500 kar do (slow)
Masla 4: DLS hamesha fail ho raha
Hal: Depth limit barhao:

python
pathfinder.dls(start, target, depth_limit=30)  # 20 ki jagah 30
📸 Screenshots Kaise Lene
Screenshots save karne ke liye:

bash
# Windows
Windows + Shift + S

# Mac
Cmd + Shift + 4

# Ya program mein save option hai
🎓 Algorithms Explained - Simple Words Mein
1. BFS (Breadth-First Search)
Kaam: Pehle paas wale check karo, phir door wale

Use: Queue

Acha: Shortest path guarantee

Bura: Zyada memory leta

2. DFS (Depth-First Search)
Kaam: Ek rasta end tak jao, phir wapas aao

Use: Stack

Acha: Kam memory leta

Bura: Shortest path nahi milta

3. UCS (Uniform Cost Search)
Kaam: Jo move sasta ho, pehle woh karo

Use: Priority Queue

Acha: Cost ke hisaab se best

Bura: Slow ho sakta

4. DLS (Depth-Limited Search)
Kaam: DFS but ek limit tak

Use: Stack + depth counter

Acha: Control hai kitna door jaana

Bura: Limit se bahar target ho toh nahi milega

5. IDDFS (Iterative Deepening DFS)
Kaam: DLS bar-bar karo, limit barha kar

Use: Loop + DLS

Acha: Memory kam, shortest path bhi milta

Bura: Thoda slow

6. Bidirectional Search
Kaam: Start se bhi search, target se bhi search

Use: Do queues

Acha: Aadha time lagta

Bura: Complex implement karna

🏗️ Project Structure
text
ai-pathfinder/
│
├── pathfinder.py          # Main code - yahan sab kuch hai
├── requirements.txt       # Dependencies ki list
├── README.md             # Yeh file jo padh rahe ho
│
├── screenshots/           # Tumhare screenshots yahan save karo
│   ├── bfs_best.png
│   ├── bfs_worst.png
│   └── ...
│
└── outputs/              # Generated reports yahan aayenge
    └── report.pdf
💻 Code Modify Karne Ke Tareeqay
Grid Size Badalna:
pathfinder.py mein yeh line dhoondo:

python
env = GridEnvironment(size=(15, 15))  # 10x10 se 15x15 kar do
Colors Badalna:
python
self.colors = {
    'empty': 'white',
    'wall': 'black',
    'start': 'purple',     # Blue ki jagah purple
    'target': 'pink',      # Green ki jagah pink
    # ...
}
Obstacles Zyada Karne:
python
obstacle_probability = 0.3  # 0.2 se 0.3 kar do
🐛 Troubleshooting - Problem Solving
Problem: pip install kaam nahi kar raha
Solution:

bash
python -m pip install --upgrade pip
python -m pip install matplotlib numpy
Problem: "python" command nahi chalta
Solution:

bash
# Windows mein try karo:
py pathfinder.py

# Mac/Linux mein try karo:
python3 pathfinder.py
Problem: GUI freeze ho jata hai
Solution: Animation speed kam karo:

python
viz.animate(delay=500)  # Slow motion
Problem: Dynamic obstacles kaam nahi kar rahe
Solution: pathfinder.py mein check karo:


🎯 Quick Commands Summary
bash
# 1. Install
pip install -r requirements.txt

# 2. Run
python pathfinder.py

# 3. Agar issue ho
python -m pip install --upgrade pip
python -m pip install matplotlib numpy
python pathfinder.py
