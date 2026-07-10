# The Ballmer Peak Eval

> A scientifically questionable benchmark for measuring whether an AI coding
> agent can compensate for a progressively degraded operator.

The original Ballmer Peak proposes a narrow band in which programmer ability
is mysteriously enhanced. AI changes the shape of that curve. A coding agent
can preserve syntax, working memory, and test discipline while its operator
introduces typos, ambiguity, contradictions, and increasingly adventurous
architectural decisions.

This benchmark measures that effect using **BAC: Behavioral Ambiguity
Coefficient**. No alcohol is required or recommended.

## Methodology

The harness runs one coding task repeatedly at increasing BAC levels. It
mutates the clean prompt, gives each mutation to an agent in a fresh workspace,
and grades the resulting code with an external test program.

| BAC | Classification | Typical prompt condition |
| ---: | --- | --- |
| 0.00 | Sober | Complete and precise |
| 0.03 | Loosened | Typos and casual wording |
| 0.06 | Ballmer candidate | Missing context and confident asides |
| 0.10 | Impaired | Contradictory implementation advice |
| 0.14 | Hammered | Reckless scope and urgency |
| 0.20 | Windows ME | Architectural free association |

The report identifies:

- **Ballmer Peak:** highest mean correctness score.
- **Confidence Cliff:** first level after the peak where mean score falls by at
  least 25 points.
- **Windows ME Event:** a run at BAC 0.14 or above that scores below 25.

## Quick start

Python 3.10 or newer is the only requirement.

```powershell
python -m ballmer_peak demo
```

The demo produces a deterministic synthetic curve so the central hypothesis
can be appreciated without spending inference tokens.

Run the included retry-client benchmark against the intentionally perfect
reference agent:

```powershell
python -m ballmer_peak run `
  --eval evals\retry-client `
  --agent-command "python examples\reference_agent.py {workspace}" `
  --repetitions 2 `
  --output results\reference.json
```

The agent command receives two placeholders:

- `{workspace}`: a fresh copy of the benchmark repository.
- `{prompt_file}`: a UTF-8 file containing the impaired prompt.

The command is trusted local code and is executed through the system shell.
An actual model adapter can read the prompt, invoke its coding agent, and let
that agent edit the workspace.

## Eval format

Each eval directory contains:

```text
evals/retry-client/
  task.json       Public task metadata and pristine prompt
  repo/           Repository copied for every run
  grader.py       External grader; never copied into the agent workspace
```

`grader.py` accepts the workspace path and prints one JSON object:

```json
{"passed": 5, "total": 5, "details": ["..."]}
```

This is not a medical instrument, a recommendation, or a meaningful reason to
drink. It is, however, benchmark-shaped.
