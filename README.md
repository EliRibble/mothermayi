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

This installs the `pylint` hook for `mothermayi`. You can get more information on pylint at it's website <insert>. Now if you perform a commit you'll see something like this:

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

Configuration
=============

Configuration of `mothermayi` is pretty straightforward. Most plugins will work correctly out of the box. Some may take configuration parameters. Simply create a `.mothermayi` file in your repository. `mothermayi` will traverse the file system all the way back to the root looking for it. When it finds one it will import it as a YAML file and provide the config to all plugins. Plugins will take their own configuration parameters - check the documentation of the plugin you care about to see what configuration values it understands. In our example with `pylint` above you could have a configuration file like this:

```
pylint:
    args:
        - --reports=no
        - --rcfile=pylint.cfg
```

This tells `pylint` to not generate reports and to use the config file at `pylint.cfg`. Well, more literally, it tells the plugin to add on the arguments `--reports=no --rcfile=pylint.cfg` when executing pylint.

Thanks
======
MotherMayI is inspired by `pre-commit` at http://pre-commit.com. I liked the idea, but I didn't like the implementation and figured with a more Python-centric approach I could make it easier to work with. We'll see if I'm right. But thanks for the cool software hackers at Yelp!

