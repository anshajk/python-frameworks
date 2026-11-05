"""Image predicates measured against real labelled photographs.

The synthetic shapes this demo originally used proved nothing: a scribble drawn
on a rectangle is not damage, and the model sensibly scored it near chance.
This version runs against real photos with ground-truth labels so the numbers
mean something.

Dataset: mohammadnajeeb/concrete_crack_images (CC-BY-4.0), 227x227 photographs
of concrete surfaces labelled Negative (no crack) / Positive (crack).

Nothing is bulk-downloaded. The Hugging Face datasets-server returns per-row
image URLs, so only the sampled images are fetched -- a few hundred KB.

Cost: a 227x227 image is ~280 input tokens, about $0.000028 per call. The
default 30-image run costs well under a cent. The estimate is printed before
any request is made.

Run:
    python image_predicate_demo.py
    python image_predicate_demo.py --limit 60
"""

import argparse
import base64
import random
import time

import httpx2 as httpx  # the OpenAI SDK ships httpx2; no extra dependency

from _common import INPUT_COST_PER_1M, MODEL, get_client, require

DATASET = "mohammadnajeeb/concrete_crack_images"
ROWS_URL = "https://datasets-server.huggingface.co/rows"

# The test split is ordered: Negative first, then Positive. These ranges stay
# clear of the boundary so a sampled offset always has the label we expect.
NEGATIVE_RANGE = (0, 3900)
POSITIVE_RANGE = (4100, 7900)

QUESTION = (
    "Does this concrete surface have a visible crack? "
    "A crack is a dark, irregular line or fracture running through the surface. "
    "Ignore stains, discolouration, surface texture, and shadows."
)

APPROX_TOKENS_PER_IMAGE = 280

# Images are drawn from several scattered blocks rather than one contiguous run:
# adjacent rows are often near-duplicate crops of the same source photograph,
# which makes the sample look easier than it is. One request per block keeps the
# unauthenticated hub rate limit happy.
BLOCKS_PER_CLASS = 5


def fetch_rows(client: httpx.Client, offset: int, length: int, attempts: int = 5):
    """Fetch a contiguous block of rows, backing off on the hub's rate limit."""
    for attempt in range(attempts):
        response = client.get(
            ROWS_URL,
            params={
                "dataset": DATASET,
                "config": "default",
                "split": "test",
                "offset": offset,
                "length": length,
            },
        )
        if response.status_code == 429:
            delay = 2**attempt
            print(f"  rate limited by the hub, retrying in {delay}s...")
            time.sleep(delay)
            continue
        response.raise_for_status()
        return response.json()["rows"]
    raise RuntimeError("Hugging Face datasets-server kept rate limiting; try again shortly.")


def sample_images(http: httpx.Client, per_class: int, seed: int):
    """Draw each class from several scattered blocks.

    Sampling offsets one at a time means one HTTP call per image, which trips the
    hub's rate limit; a single contiguous block risks near-duplicate crops. A few
    scattered blocks gets diversity at a handful of requests.
    """
    rng = random.Random(seed)
    samples = []
    for label, (low, high) in ((0, NEGATIVE_RANGE), (1, POSITIVE_RANGE)):
        remaining = per_class
        for block in range(BLOCKS_PER_CLASS):
            size = remaining if block == BLOCKS_PER_CLASS - 1 else max(1, per_class // BLOCKS_PER_CLASS)
            size = min(size, remaining)
            if size <= 0:
                break
            start = rng.randrange(low, high - size)
            for row in fetch_rows(http, start, size):
                if row["row"]["label"] != label:
                    continue
                samples.append((row["row"]["image"]["src"], label))
            remaining -= size
    rng.shuffle(samples)
    return samples


def download_image(http: httpx.Client, url: str) -> bytes:
    response = http.get(url)
    response.raise_for_status()
    return response.content


def evaluate(scored, threshold):
    tp = sum(1 for gold, p in scored if gold == 1 and p >= threshold)
    fp = sum(1 for gold, p in scored if gold == 0 and p >= threshold)
    fn = sum(1 for gold, p in scored if gold == 1 and p < threshold)
    tn = sum(1 for gold, p in scored if gold == 0 and p < threshold)
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / len(scored) if scored else 0.0
    return precision, recall, f1, accuracy, fp, fn


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=30, help="total images to score (default 30)")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    per_class = max(1, args.limit // 2)
    total = per_class * 2
    estimate = total * APPROX_TOKENS_PER_IMAGE / 1_000_000 * INPUT_COST_PER_1M
    print(f"Dataset : {DATASET} (CC-BY-4.0)")
    print(f"Sampling: {per_class} cracked + {per_class} intact = {total} images")
    print(f"Estimated API cost: ${estimate:.6f}\n")

    client = get_client()
    http = httpx.Client(timeout=60, follow_redirects=True)
    print("Fetching image URLs...")
    samples = sample_images(http, per_class, args.seed)
    print(f"Got {len(samples)} images. Scoring...\n")

    scored = []
    spent = 0.0
    for index, (url, gold) in enumerate(samples, start=1):
        encoded = base64.b64encode(download_image(http, url)).decode("ascii")
        decision = client.decisions.create(
            model=MODEL,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "Inspect this concrete surface."},
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{encoded}"},
                    ],
                }
            ],
            questions=[{"type": "predicate", "name": "has_crack", "instructions": QUESTION}],
        )
        probability = require(decision, "has_crack").probability
        spent += decision.usage.input_tokens / 1_000_000 * INPUT_COST_PER_1M
        scored.append((gold, probability))

        gold_label = "CRACKED" if gold else "intact "
        predicted = "crack" if probability >= 0.5 else "clean"
        correct = (probability >= 0.5) == bool(gold)
        print(
            f"  {index:>3}. p={probability:.2f}  gold={gold_label}  "
            f"pred={predicted}  {'ok' if correct else 'MISS'}"
        )

    print(f"\nActual spend: ${spent:.6f} ({len(scored)} calls)")

    print(f"\n{'thresh':>7} {'prec':>6} {'recall':>7} {'F1':>6} {'acc':>6} {'FP':>4} {'FN':>4}")
    print("-" * 44)
    rows = []
    for step in range(1, 20):
        threshold = step / 20
        precision, recall, f1, accuracy, fp, fn = evaluate(scored, threshold)
        rows.append((threshold, f1, accuracy))
        print(
            f"{threshold:>7.2f} {precision:>6.2f} {recall:>7.2f} {f1:>6.2f} "
            f"{accuracy:>6.2f} {fp:>4} {fn:>4}"
        )

    best = max(rows, key=lambda r: r[1])
    at_half = next(r for r in rows if abs(r[0] - 0.50) < 1e-9)
    print(f"\nBest F1 {best[1]:.2f} at threshold {best[0]:.2f} (accuracy {best[2]:.2f})")
    print(f"At the naive 0.50 default: F1 {at_half[1]:.2f}, accuracy {at_half[2]:.2f}")


if __name__ == "__main__":
    main()
