*This project has been created as part of the 42 curriculum by nyramana.*

# Call Me Maybe

<!--toc:start-->
- [Call Me Maybe](#call-me-maybe)
  - [Description](#description)
  - [Instructions](#instructions)
    - [Makefile](#makefile)
    - [Manual](#manual)
  - [Resources](#resources)
    - [AI Usage](#ai-usage)
  - [Extras](#extras)
    - [Algorithm explanation](#algorithm-explanation)
    - [Design decisions](#design-decisions)
    - [Performance analysis](#performance-analysis)
    - [Challenges faced](#challenges-faced)
    - [Testing strategy](#testing-strategy)
    - [Example usage](#example-usage)
<!--toc:end-->

## Description

**Call me maybe** is a project that introduces LLM generation and constrained decoding.

The goal of this project is simple: generate the name and parameters of a function that solve requests or prompts by using the LLM and constrained decoding. This way we don't rely solely on the LLM but guide it to generate valid answers.

An example of constrained decoding:

- Prompt: "reverse the word: 'you are beautiful'."
- Answer without constrained decoding:
  - the reverse of the word 'you are beautiful' is 'lufituaeb era uoy'.
- Answer with constrained: "answer":
  - "lufituaeb era uoy"

So this program will follow this constrained decoding method to generate valid data and output the value in a json file.

## Instructions

> [!NOTE]
> This program will store +5 Gb in the memory, be prepared to download it and configure your settings.

- To change where the UV will store its cache:

```bash
export HF_HOME="/home/$(USER)/goinfre/.cache/huggingface"
export UV_CACHE_DIR="/home/$(USER)/goinfre/.uv_cache"

```

### Makefile

- To install dependencies:

```bash
make install # or make
```

- To run the program:

```bash
make run
```

- To debug:

```bash
make debug
```

- To clean caches:

```bash
make clean
```

- To check code quality:

```bash
make lint
make lint-strict
```

### Manual

- To install dependencies:

```bash
uv sync
```

- To run the program:

```bash
uv run python3 -m src [–-functions_definition <function_definition_file>] [–-input <input_file>] [–-output <output_file>] [--bonus]
```

All parameters are optional and have default values.

- **functions_definition**: File containing all function declarations.
- **input**: File containing prompts or inputs.
- **output**: File that will store the result of the program.
- **Bonus**: Flag to run the bonus program.

> [!IMPORTANT]
> If you are launching the bonus, you will need to choose between two models before generation starts

## Resources

- **Peer learning.**
- [Constrained decoding](https://youtu.be/xpvFinvqRCA?si=y2c4_kxCeAlTdxVu)
- [Huggingface](https://huggingface.co/)

### AI Usage

AI was generally used to explain some regular expression syntax and to show how to use the *rich* library in Python. It also helped me understand the state machine.

## Extras

### Algorithm explanation

Constrained decoding is a very efficient method to always output a valid value. To implement that in my project, there were two main design choices:

- First, to generate the function name, I used a method where instead of deleting every forbidden syntax, I only check the allowed one. This is done to optimize the generation and minimize resource utilization.

**Example**:

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
prompt = "What is 2 multiply by 1?"
encoded_prompt = model.encode(prompt).tolist()[0]
func_name = ["fn_add_numbers", "fn_mult", "fn_greet"]

# We transform every name into tokens
func_name_tokens = [[8822, 2891, 32964], [8822, 26290], [8822, 1889, 3744]]
# Get the logits from the LLM
logits = model.get_logits_from_input_ids(encoded_prompt)

# Instead of checking every input, we only check what we need
valid_tokens = {seq[0] for seq in func_name_tokens}

best = float("-inf")
token_id = -1
# This will output {8222}
for token in valid_tokens:
    # Get the value of the token.
    if best < logits[token]:
        best = logits[token]
        token_id = token

# After that, we get the best value with constrained decoding.
print(f"{model.decode([token_id])} is the best match for the llm with constrained decoding.")

```

- Second, To generate the parameters of the function, I used a finite state machine. A finite state machine or FSM is a popular concept in video games and algorithm implementation. It switch between a state and each state can do one thing at a time. This is done to make sure the LLM always generates valid data because we tell it what to do.

**Example**:

```bash
INTEGER:
    START (+, -, NUMBER)
    INTEGER (NUMBER)
    END ('"', ...)

FLOAT:
    START (+, -, NUMBER)
    INTEGER (NUMBER)
    DOT (.)
    DECIMAL (NUMBER)
    END ('"', ...)
```

### Design decisions

```bash
 src
├──  __init__.py
├──  __main__.py
├──  llm
│   ├──  __init__.py
│   ├──  custom_llm.py
│   ├──  generator.py
│   ├──  statemachine
│   │   ├──  __init__.py
│   │   ├──  base.py
│   │   ├──  integer.py
│   │   ├──  number.py
│   │   └──  string.py
│   └──  tokenizer.py
├──  model
│   ├──  __init__.py
│   ├──  input.py
│   └──  output.py
├──  parsers
│   ├──  __init__.py
│   ├──  checker.py
│   ├──  loader.py
│   └──  saver.py
└──  ui
    ├──  __init__.py
    └──  home.py
```

I added a lot of implementation in this project. First is the state machine and selective decoding explained above. I also added the *parsers* module that stores classes to make loading and saving easier (it includes error handling to verify if a file is available before continuing).

The *model* package contains validation logic for program inputs and outputs. This ensures that data is structured and scalable.

The *llm* package contains the core of the project: classes to run the custom LLM with constrained decoding, a simple tokenizer, and a generator for four specific types: number, integer, boolean, and string. Objects like arrays or nested function arguments are not handled and are treated as strings by default to keep the project scope limited.

### Performance analysis

This project uses **Qwen/Qwen3-0.6B** as the default LLM. This model is lightweight and can be used on a normal computer, so the program is fairly fast (between 60 and 90 seconds) to run the default prompt.

Accuracy depends on the prompt, because the LLM has no complex reasoning. It relies on the best allowed value, and the LLM doesn't always understand the prompt, so it can generate other values and miss the real goal. It can be reliable if the prompt is clear, but may struggle with complex or ambiguous requests.

### Challenges faced

There were many difficulties encountered during this project. The topic was unclear at first and there was limited documentation. Peer learning helped me understand the basics, after which I explored solutions independently. I tried some community suggestions that were not suitable for my approach, so I ran my own tests and found alternative (not always better) implementations. I also tested FSM edge cases with colleagues. One remaining issue is negative integers: the LLM rarely generates them because the most probable answer tends to be a positive number.

### Testing strategy

I tested my implementation using the project's own tests and they passed. I then tried harder cases and it worked for most, but still fails on some complex inputs. I also experimented with changing function names, parameters, and descriptions, and most changes produced acceptable results.

### Example usage

To run the program, first you need two files: a list of prompts as JSON (see data/input/function_calling_tests.json) and a list of function definitions as JSON (see data/input/functions_definition.json). You can change these values using flags when launching the program. These files will be loaded in JSON format and validated by the model in *src/model/input.py*.

The program will start generating function names and parameters using the LLM, and results are saved in a JSON file (default: data/output/function_call_results.json).

You can create your own prompts and function definitions by following the format below:

**Prompt file**:

```json
[
    {
        "prompt": "..."
    },
    {
        "prompt": "..."
    }
]
```

**Functions Definition**:

```json
{
    "name": "...",
    "description": "...",
    "parameters": {
        ...
        },
    "returns": {
        "type": "..."
        }
}
```
