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

**Call me maybe** is a wonderful project that introduce LLM generation and constrained decoding.

The **Goal** of this project is simple: Generate the name and parameters of the function that solve the request or prompt by using the llm and constrained decoding. So we don't rely on the llm itself but guide him to generate valid answer.

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

- To change where the UV will store his cache:

```bash
export HF_HOME="/home/$(USER)/goinfre/.cache/huggingface"
export UV_CACHE_DIR="/home/nyramana/goinfre/.uv_cache"

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
make lint-strinct
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

Every parameters are optionals and has a default value.

- **functions_definition**: The file that contains every declaration of function.
- **input**: The file that contains every declaration or prompts.
- **output**: The file that will store the result of the program.
- **Bonus**: Flag to run the bonus program.

> [!IMPORTANT]
> If you are launching the bonus, You will need need to choose between two model before the generation is starting

## Resources

- **Peer learning.**
- [Constrained decoding](https://youtu.be/xpvFinvqRCA?si=y2c4_kxCeAlTdxVu)
- [Huggingface](https://huggingface.co/)

### AI Usage

AI was used generally to explain some regular expression syntaxes and to tell me how to use the *rich* library in python. It also helps me understanding the state machine.

## Extras

### Algorithm explanation

Constrained decoding is a very efficient method to always output a valid value. To implement that to my project, there was two main design:

- First, to generate the function name, I used a method where instead of deleting every forbidden syntax, I only check the allowed one. This is done to optimize the generation and minimize resource utilization.

**Example**:

```python
from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
prompt = "What is 2 multiply by 1?"
encoded_prompt = model.encode(prompt).tolist()[0]
func_name = ["fn_add_numbers", "fn_mult", "fn_greet"]

# We transform every name in token
func_name_tokens = [[8822, 2891, 32964], [8822, 26290], [8822, 1889, 3744]]
# Get the logits from the llm
logits = model.get_logits_from_input_ids(encoded_prompt)

# Instead of checking every input, we only check only what we need
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

- Second, To generate the parameters of the function, I used a finite state machine. A finite state machine or FSM is a popular concept in video games and algorithm implementation. It switch between a state and each state can do one thing at a time. This is done to make sure the LLM always generate a valid data because we tell them what they should do.

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

I added a lot of implementation in this project. First is the State machine and selective decoding I explained above. I also added the *parsers* file that store class to make loading and saving easier (It has error handling to verify if the file is available or not before continuing) .

The *model* package stores every model validation for the input and output of the program. This ensure that every data is structured and scalable.

The *llm* file contains be core of the project, here belongs the class to run of the custom llm with constrained decoding, simple tokenization class and generator with 4 specific type: The number, the integer, the boolean and string. Object like array or nested function arguments was not handled and considered string by default to keep the program from scope.

### Performance analysis

This model used **Qwen/Qwen3-0.6B** as a default llm. This model is lightweight and can be used with a normal computer. So the program is pretty fast (between 60 sec and 90 sec) to run the default prompt.

The accuracy is based on the prompt, because the llm has no complex implementation. It rely on the best value if it is allowed, and the llm don't always understand the prompt so it can generate other value and miss the real goal. So It can be really reliable if your prompt is good, but have some challenge when it comes to complex request or blurry prompt.

### Challenges faced

There was a lot of difficulty encountered with this project, The project was not clear at first and there were not a lot of subject on documentation about it. Then the peer learning helped me to know the basics and then I went on my own. On my way, I tried to implement what other people said and it was not the right approach for me, so I did my own test and found other (not always better) way to implement the logic. Then I finished with the FSM test some edge cases with my friends. There is also a problem that is not really solved because it rely on the llm which is the negative integer, the llm cannot generate it because the most probable answer is always a number.

### Testing strategy

I tested my implementation by using the project own test and it worked. Then I tried with some harder one and it did fine on most of them but still fail for some complex one.
I also tried to change function name, parameters, and description and it made most of them.

### Example usage

To run the program, First you need to have 2 file, the list of prompt as a json (see data/input/function_calling_tests.json file) and the list of function definition as a json (see data/input/functions_definition.json). You can change the value by using a flag when launching the program. These file will be loaded as a json format and will be validated by the model in *src/model/input.py* file.

The program will start generating the function name and parameters using the llm. And will be saved in a json file (default in data/output/function_call_results.json)

You can create your own prompt and function definitions by following the format bellow:

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
