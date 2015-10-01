MotherMayI
==========

`mothermayi` is a module and system for creating git pre-commit hooks. A pre-commit hook is a script that runs before your commit is made and commonly used to verify or improve code. `mothermayi` provides a means to create a simple pre-commit hook and then add-on modules that provide the desired behavior

Getting Started
===============

You can get started with `mothermayi` by using PIP:

```
pip install mothermayi
```

This can be done in a virtual environment or at the system level. Once you've done that you install the commit hook in your git repo.

```
cd my/git/repo
mothermayi install
```

You now have a pre-commit hook at `.git/hooks/pre-commit` which will be run any time you make a commit. However, that hook does nothing interesting. You'll need some action for it to take. For that you'll want to install one or more plugins

```
pip install mothermayi-pylint
```

This installs the `pylint` hook for `mothermayi` (https://github.com/EliRibble/mothermayi). You can get more information on pylint at it's website at http://www.pylint.org/. Now if you perform a commit you'll see something like this:

```
$ git commit
pylint    ...[PASSED]
```

That shows you that `mothermayi` ran your pylint hook and everything passed. The odds of that happening your first time are slim, so here's what you're much more likely to see

```
$ git commit
pylint    ...[FAILED]
************* Module test
test.py:3: [W0301(unnecessary-semicolon), ] Unnecessary semicolon
```

This tells you that the module `test.py` failed the pylint test. Cool!

List of Known Plugins
=====================

If your plugin is not listed here please update the project via pull request or issue

- https://github.com/EliRibble/mothermayi-example - The example plugin to help you get started writing your own
- https://github.com/EliRibble/mothermayi-isort - A plugin for checking imports are sorted
- https://github.com/EliRibble/mothermayi-pylint - A plugin for running pylint against your code

Configuration
=============

Configuration of `mothermayi` is pretty straightforward. Most plugins will work correctly out of the box. Some may take configuration parameters. Simply create a `.mothermayi` file in your repository. `mothermayi` will traverse the file system all the way back to the root looking for it. When it finds one it will import it as a YAML file and provide the config to all plugins. Plugins will take their own configuration parameters - check the documentation of the plugin you care about to see what configuration values it understands. In our example with `pylint` above you could have a configuration file like this:

```yaml
pylint:
    args:
        - --reports=no
        - --rcfile=pylint.cfg
```

This tells `pylint` to not generate reports and to use the config file at `pylint.cfg`. Well, more literally, it tells the plugin to add on the arguments `--reports=no --rcfile=pylint.cfg` when executing pylint.

Creating a plugin
=================

The whole point of `mothermayi` is to make it easier to create plugins. You can check out an example plugin for yourself at https://github.com/EliRibble/mothermayi-example/ The fundamental elements of a plugin are as follows:

1. A setup file with a proper entry_point
2. A function that returns the plugin data
3. A function that can handle the hook

The entry point
---------------

The entry point is how your plugin registers itself with `mothermayi`. You can read about them at http://pythonhosted.org/setuptools/pkg_resources.html#entry-points. In general it will look kind of like this:

```python
from setuptools import setup

def main():
    setup(
        ...
        entry_points = {
            'mothermayi'    : [
                'plugin = mmiexample.main:plugin',
            ]
        }
        ...
    )
```

That is, you'll pass in a parameter to `setup` called `entry_points`. It should be a dict with a key in it called `mothermayi`. This is how `mothermayi` will find your entry_point. From there you can call you entry point anything you like - I've called mine `plugin`. It references a module in a package, `mmiexample.main` and a particular function in that module, `plugin`. This function will be called when `mothermayi` loads in order to get information about the plugin.

A function that returns the plugin data
---------------------------------------

Here's what my plugin function looks like:

```python
def plugin():
    return {
        'name'          : 'example',
        'pre-commit'    : pre_commit,
    }

def pre_commit(config, staged):
    ...
```

I'll get to the definition of `pre_commit` in a second. For now we'll focus on `plugin`. The `name` property that it returns is the name that will be displayed when `mothermayi` runs and should allow users to identify the plugin. If two plugins load with the same name from separate entry_points `mothermayi` will abort. So try to make it reasonably unique as well.

Next the dict contains mappings of git hook types to functions that can handle those hooks. In this case I only have one, a `pre-commit` hook that will cause my function to be called. Each type of hook has a different function signature

A function that can handle the hook
-----------------------------------

Right now `mothermayi` only supports `pre-commit` hooks. In the future it will support more. Each hook takes a different set of parameters. They all take a config, which will contain the configuration file that `mothermayi` loads as a `dict`. The `pre-commit` hook also takes in a list of files that will be committed (ie, files that are currently staged). This allows the hook to easily operate on those files without having to determine them itself.

The hook function can do anything - analyze the files, change them, stage the new changes, etc. In order to signal that the hook should abort the commit it should raise `mothermayi.errors.FailHook`. Any message put into the constructor of the exception will be displayed to the user as the reason the hook failed. If the hook is successful it can return a string that will also be displayed to the user to provide status information. If you want to get fancy there's a `mothermayi.colors` module for coloring that output in a convenient way

Deployment
----------

With that your hook is done. All you need to do is deploy it. I'd recommend PyPI (https://pypi.python.org/pypi) for that. The example plugin has a `setup.py` file that has enough data in it for you to use it to register your plugin with PyPI via `python setup.py register` and `python setup.py sdist upload`. If you let me know about your plugin via an issue in github or a pull-request we'll add it to the list of plugins

Thanks
======
MotherMayI is inspired by `pre-commit` at http://pre-commit.com. I liked the idea, but I didn't like the implementation and figured with a more Python-centric approach I could make it easier to work with. We'll see if I'm right. But thanks for the cool software hackers at Yelp!

