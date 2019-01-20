# Text Transformer

A tool that can transform ASCII text with help of Python user code.

- [Requirements](#requirements)
- [Usage](#usage)
  - [Example transformer](#example-transformer)
- [Files of interest](#files-of-interest)
  - [txttrans.pyw](#txttranspyw)
  - [transformers.py](#transformerspy)
  - [config.py](#configpy)
  - [api.py](#apipy)
    - [Members](#members)
      - [`api.transformer`](#apitransformer)
      - [`api.message`](#apimessage)
      - [`api.SimpleDataDialog` and `api.DataEntry`](#apisimpledatadialog-and-apidataentry)
      - [`api.execdir`](#apiexecdir)
- [Copyright and License](#copyright-and-license)


## Requirements

[Python 3.6](https://www.python.org/) is needed.

The transformer file imports some modules that are not part of the Python distribution. See [transformers.py](transformers.py) for details. It was considered to keep transformers still usable if they do not need these external modules.


## Usage

See [transformers.py](transformers.py) for examples. You can add so called "transformers" there. A "transformer" takes the text that is currently in the main text field as parameter and returns some other text.

You can change, add and delete transformers while the tool is running.


### Example transformer

```python
@api.transformer("Say hello")
def t(text):
    return "Hello " + text
```

For transform functions that consist only of one line, this syntax can be used alternatively:

```python
api.transformer("Say hello")(lambda text: "Hello " + text)
```


## Files of interest

### [txttrans.pyw](txttrans.pyw)

File to start the tool.


### [transformers.py](transformers.py)

[Described above](#example-transformer).


### [config.py](config.py)

Configuration file. It allows you to alter the appearance of the tool and and switch on/off the debug mode (consists of additional messages).


### [api.py](api.py)

Members of this module are supposed to be invoked by transformers. It should never be necessary to invoke methods of other modules of the application (e.g. `gui` or `info`).


#### Members

##### `api.transformer`

Described above.


##### `api.message`

Message system of the application to output messages in the message area. Different kind of messages can be generated. Each message method can be given an arbitrary count of arguments that are separated by the `sep` argument.

Example:

```python
api.message.info("This", "is a", "message separeted by", "line breaks", sep="\n")
```

- `api.message.debug`: This message line is only generated, if the debug switch in "config.py" is set to `True`
- `api.message.info`: For information
- `api.message.warn`: To generate warnings
- `api.message.error`: To say if something went wrong


##### `api.SimpleDataDialog` and `api.DataEntry`

A dialog to enter some data that may be needed by a Transformer. It consists of some text boxes to enter data and a label for each text box.

Example:

```python
@api.transformer("Say Hello")
def t(text):
    entries = [
        api.DataEntry("Forename", validator=lambda value: value == "Tom"),
        api.DataEntry("Surname", "Jones", validator=bool),
        api.DataEntry("No meaning"),
    ]
    sdd = api.SimpleDataDialog("Hello", entries)
    if not sdd.canceled:
        result = sdd.result
        return "Hello {} {}".format(result["Forename"], result["Surname"])
```

An `api.DataEntry` needs at least one argument - the value name. This value name appears as label for the corresponding text box and is used to address the corresponding value.

The second, optional argument is the default value that appears in its text box.

Additionally, a validator function can be given. This validator is executed when the user clicks on the OK button. It gets the text box value as parameter and is expected to return either `True` or `False`, depending on the criteria for the value. If you just want to validate that the text box is not empty, you can say `validator=bool` as in the second `api.DataEntry` in the example above.

`api.SimpleDataDialog` expects the dialog title as first parameter and the `api.DataEntry`s as second parameter. A call to `api.SimpleDataDialog` will return a dialog object, containing the result dictionary. The keys of this result dictionary are the value names (first parameter of `api.DataEntry`). The dialog object has a member `cancaled`, indicating whether the user closed the dialog via "Cancel" (or the close button of the window manager).


##### `api.execdir`

Directory where the tool (txttrans.pyw) is. Useful e.g. to put some files there that can be used by a transform handler.


## Copyright and License

This tool is made by Christian Dreier. If you find a copy somewhere, you find the original at [GitHub](https://github.com/c3er/txttrans).

You can use and copy this tool under the conditions of the MIT license.
