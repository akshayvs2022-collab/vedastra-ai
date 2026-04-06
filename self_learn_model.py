"""Continue training the project's current text model.

This script is built for the existing artifacts in this repository:
- model.pkl
- vectorizer.pkl

It lets you keep learning from newly labeled examples without retraining from scratch.
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path


class CurrentModelTrainer:
    """Incrementally train the project's current model/vectorizer artifacts."""

    def __init__(self, model_path: str = "model.pkl", vectorizer_path: str = "vectorizer.pkl") -> None:
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.model = self._load_pickle(self.model_path)
        self.vectorizer = self._load_pickle(self.vectorizer_path)

        if self.model is None or self.vectorizer is None:
            raise FileNotFoundError(
                "Could not load existing artifacts. Make sure model.pkl and vectorizer.pkl exist."
            )

        if not hasattr(self.model, "partial_fit"):
            raise TypeError(
                "Loaded model does not support incremental updates (partial_fit)."
            )

    @staticmethod
    def _load_pickle(path: Path):
        with path.open("rb") as file:
            return pickle.load(file)

    def predict(self, text: str) -> str:
        x = self.vectorizer.transform([text])
        return str(self.model.predict(x)[0])

    def learn(self, text: str, label: str) -> None:
        """Learn one new example and keep class list stable from existing model."""
        x = self.vectorizer.transform([text])

        classes = getattr(self.model, "classes_", None)
        if classes is None:
            raise RuntimeError(
                "Existing model has no classes_. Train once first before incremental updates."
            )

        self.model.partial_fit(x, [label], classes=classes)

    def save(self, model_out: str | None = None, vectorizer_out: str | None = None) -> tuple[Path, Path]:
        model_target = Path(model_out) if model_out else self.model_path
        vectorizer_target = Path(vectorizer_out) if vectorizer_out else self.vectorizer_path

        with model_target.open("wb") as file:
            pickle.dump(self.model, file)

        with vectorizer_target.open("wb") as file:
            pickle.dump(self.vectorizer, file)

        return model_target, vectorizer_target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update current trained model (model.pkl + vectorizer.pkl) with one new example."
    )
    parser.add_argument("--text", required=True, help="Input text to learn from")
    parser.add_argument("--label", required=True, help="Correct label/answer for the input text")
    parser.add_argument("--model-path", default="model.pkl", help="Path to current model pickle")
    parser.add_argument(
        "--vectorizer-path",
        default="vectorizer.pkl",
        help="Path to current vectorizer pickle",
    )
    parser.add_argument(
        "--model-out",
        default=None,
        help="Optional output model path. Default overwrites --model-path",
    )
    parser.add_argument(
        "--vectorizer-out",
        default=None,
        help="Optional output vectorizer path. Default overwrites --vectorizer-path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    trainer = CurrentModelTrainer(model_path=args.model_path, vectorizer_path=args.vectorizer_path)

    before = trainer.predict(args.text)
    trainer.learn(args.text, args.label)
    after = trainer.predict(args.text)

    model_saved, vectorizer_saved = trainer.save(
        model_out=args.model_out,
        vectorizer_out=args.vectorizer_out,
    )

    print(f"Before learning: {before}")
    print(f"After learning:  {after}")
    print(f"Model saved: {model_saved}")
    print(f"Vectorizer saved: {vectorizer_saved}")


if __name__ == "__main__":
    main()