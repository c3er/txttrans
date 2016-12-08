A tool that can transform ASCII text with help Python code.

# Usage

See [transformers.py](transformers.py) for examples. You can add so called "transform_handlers" there that take the text that is currently in the main text field as parameter and returns some other text.

## Example transformer

```python
@gui.transform_handler("Say hello")
def say_hello(text):
    return "Hello " + text
```
