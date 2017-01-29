A tool that can transform ASCII text with help Python code.


# Usage

See [transformers.py](transformers.py) for examples. You can add so called "transform_handlers" there that take the text that is currently in the main text field as parameter and returns some other text.


## Example transformer

```python
@gui.transform_handler("Say hello")
def say_hello(text):
    return "Hello " + text
```


# Files of interest


## [txttrans.py](txttrans.py)

File to start the tool.


## [transformers.py](transformers.py)

Described above.


## [config.py](config.py)

Configuration file. It allows you to alter the appearance of the tool and and switch on/off the debug mode (consists of additional messages).


## [info.py](info.py)

Contains information of the environment, e.g. the directory where the starter file ([txttrans.py](txttrans.py)) is in.
