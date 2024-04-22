# llamacpp-retokenizer
Temporary solution to use the reference tokenizer while tokenizer broken in llama.cpp.

Works as a reverse proxy server. Should be compatible with any OpenAI-compatible servers, not only llama.cpp server - it just encodes prompt into tokens. Make sure you are using the correct tokenizer.

## Installation
```sh
pip3 install git+https://github.com/sasha0552/llamacpp-retokenizer.git
```
*I recommend doing it in a virtual environment.*

## Usage
1. Create `config.json` in some directory. An example configuration is available at [config.example.json](config.example.json).
2. Download `tokenizer_config.json` and `tokenizer.json` to the same directory.  
  *For example, [tokenizer_config.json](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/blob/main/tokenizer_config.json) and [tokenizer.json](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/blob/main/tokenizer.json) for Llama 3.*  
  *You can change the location of these files in the `config.json` file.*
3. Use the terminal to navigate to that directory, then run the reverse proxy using `retokenizer`.  
  *Don't forget to activate the virtual environment if necessary.*  
  *You can start the reverse proxy from any directory by specifying the `CONFIG_PATH` environment variable.*
4. Use a reverse proxy instead of llama.cpp server.
