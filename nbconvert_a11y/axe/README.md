# testing axe in python

the `test_axe` module provides utilities for running `axe-core` on html document in python. it is designed for asynchronous interactive use and synchronous testing with the `pytest_axe` extension.

`axe-core` is a javascript module that must be run inside of a live browser. currently, `playwright` is the only browser automation supporter, but `selenium` could be added.

<!-- can we add it to robots from jupyter after that? -->

## axe exceptions in python

each release contains a version of axe and a set of exceptions generated for that specific version.
the types are useful in accounting for expected accessibility that can be fixed later.

## playwright testing

it turns out the best ergonomics with working with axe from playwright are to append methods to the `Page` class. it has the following methods when `test_axe` is active:

`Page.axe`
: run axe and return the test results as a python dictionary

`Page.test_axe`
: run axe and return the test results as a python exception group

`Page.aom`
: an alias to the soon to be deprecated `page.accessibility.snapshot()`

we have to main synchronous and asynchronous methods for playwright