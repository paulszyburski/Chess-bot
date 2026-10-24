# Chess bot

A Python chess engine with a neural network trained on chess games. The bot ranks legal moves, plays out short continuations, and compares the resulting positions by material.

Use Python 3.12 or newer. Run these commands from the project folder:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

On Windows, activate with `.venv\Scripts\activate`.

The default game is you against the bot. Play as White by typing moves like `e2 e4`. Type `q` to quit.

The repo includes a lightweight trained model (about 27 MB) at `src/data/chess_model.joblib`. This is the newest saved model and loads automatically. No training or extra download is needed.

- `python src/main.py watch` runs a game between two bots.
- `python src/main.py board` opens a Pygame board preview. Mouse controls are unfinished.
- `PYTHONPATH=src python -m bot.nn` trains a new model from `.pgn` or `.pgn.zst` files in `src/data` and replaces the default model. Training limits are in `src/bot/nn.py`.
- `PYTHONPATH=src python -m bot.create_dataset < games.pgn` saves positions and moves to `lichess_training_data.npz`.

The engine supports castling, checkmate, stalemate, and queen promotion. En passant, underpromotion, repetition, and the fifty-move rule are not implemented.

Run checks with `PYTHONPATH=src python -m unittest discover -s tests`.
