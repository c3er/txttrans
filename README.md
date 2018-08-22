# Text Transformer

A tool that can transform ASCII text with help of Python code.

- [Requirements](#requirements)
- [Usage](#usage)
  - [Example transformer](#example-transformer)
- [Files of interest](#files-of-interest)
  - [txttrans.pyw](#txttranspyw)
  - [transformers.py](#transformerspy)
  - [config.py](#configpy)
  - [api.py](#apipy)
- [Copyright and License](#copyright-and-license)


## Requirements

[Python 3.6](https://www.python.org/) is needed.

The transformer file imports some modules that are not part of the Python distribution. [transformers.py](transformers.py) for details. It was considered to keep transformers still usable if they do not need these external modules.


## Usage

See [transformers.py](transformers.py) for examples. You can add so called "transformers" there. A "transformer" takes the text that is currently in the main text field as parameter and returns some other text.

You can change, add and delete transformers while the tool is running.


### Example transformer

```python
@api.transformer("Say hello")
def t(text):
    return "Hello " + text
```


## Files of interest

### [txttrans.pyw](txttrans.pyw)

File to start the tool.


### [transformers.py](transformers.py)

Described above.


### [config.py](config.py)

Configuration file. It allows you to alter the appearance of the tool and and switch on/off the debug mode (consists of additional messages).


### [api.py](api.py)

Members of this module are supposed to be invoked by transformers. It should never be necessary to invoke methods of other modules of the application (e.g. `gui` or `info`).

## Copyright and License

This tool is made by Christian Dreier. If you find a copy somewhere, you find the original at [GitHub](https://github.com/c3er/txttrans).

You can use and copy this tool under the conditions of the MIT license.
