# pyrat-engine
Repository for different PyRat game engine implementations. CPP/Python based project.

# Implementations
I intend to implementations of the engines in both Python and CPP, making them all available in Python through Python bindings.
These are the implementations on the roadmap :

| Language | Variant    | Implemented | Description                                                      |
|----------|------------|-------------|------------------------------------------------------------------|
| Python   | Naive      | :x:         | Simple reimplementation of the original code                     |
| Python   | Vectorized | :x:         | Implementation in pure Jax to allow running on GPU/TPUs natively |
| Python   | Jax        | :x:         | Implementation in pure Jax to allow running on GPU/TPUs natively |
| CPP      | Naive      | :x:         | Simple reimplementation of the original code in cpp              |
| CPP      | Vectorized | :x:         | Vectorized CPP implementation                                    |
| CPP      | Bitsets    | :x:         | Implementation using bitsets to handle game data and logic       |

# API
All implementations will provide a common interface :
- `init(width, height, player_positions = None, MazeState = None, CheeseState = None)` : Init a game (signature tbd)
- `move(p1_move, p2_move)` : make player moves.
- `unmake(p1_move,p2_move, cheeses: List[coordinates] = None)` : unmake the player moves. Optionally place back the list of cheeses.
- `set_state(State)` : set the state of the game to a given.
- `get_state()` : get the state of the current game.

# Installation
- Install the latest version :
 ```bash
 python -m pip install git+https://github.com/mintiti/pyrat-engine.git
  ```
- dev dependencies :
```bash
python -m pip install -e .[dev]
```

# Benchmarks
*Coming Soon* :tm:
