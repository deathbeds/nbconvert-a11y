from unittest import TestLoader


collect_ignore = ["notebooks/lorenz.ipynb"]

TestLoader.testMethodPrefix = "test", "xfail"
