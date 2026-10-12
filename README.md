# Monte-Carlo Economy Simulator

### Table of Contents

1. Whats That?

2. How it works?

3. Were LLMs used? (yes, but how?)

4. Predictions!

---

### 1. Whats That?

This is a Monte Carlo Simulation of International Economy with continuous statistics (such as GDP) and discrete non-linear events (such as migration crisis).

It is created with an idea to determine most probable events or statistics changes, based on massive number of semi-random scenarios.

---

### 2. How it works?

In simplest terms, we tune predicting model on historic data ($H_{i}$) in `Tunning Phase`, then we make `3 steps` for each `predictive iteration`.

#### Variables

- $H_{i}$ - Historic i-th iteration
- $P_{i, n}$ - n-th Predicted i-th iteration

#### Pre-Iterating Step (`Tunning`)

This is a step, when we train regression, for each country present in the model, on historic data.

#### Iteration Step 1 (`Large Amount of Random Changes`)

We create Large Amount of Random Changes, based on the last iteration in historic data, creating in this way $N$ scenarios.

Each Scenario consist of adding random noise to the last historic iteration ($H_{last}$).

#### Iteration Step 2 (`Predicting next Time-Steps`)

We predict next iterations $P_{i, n}$ based on Scenarios of $H_{last}$ or $P_{i-1, n}$.

Here we can go to `Step 3` or repeat from `Step 1`.

#### Iteration Step 3 (`Calculate Probability of Events`)

We calculate probability of occuring of each event, with distribution of each statistics.