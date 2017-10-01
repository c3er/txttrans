A tool that can transform ASCII text with help Python code.


# Usage

See [transformers.py](transformers.py) for examples. You can add so called "transformers" there. A "transformer" takes the text that is currently in the main text field as parameter and returns some other text.


## Example transformer

```python
@api.transformer("Say hello")
def t(text):
    return "Hello " + text
```


# Files of interest


## [txttrans.pyw](txttrans.pyw)

File to start the tool.


## [transformers.py](transformers.py)

Described above.


## [config.py](config.py)

Configuration file. It allows you to alter the appearance of the tool and and switch on/off the debug mode (consists of additional messages).


## [api.py](api.py)

Members of this module are supposed to be invoked by transformers. It should never be necessary to invoke methods of other modules of the application (e.g. `gui` or `info`).
