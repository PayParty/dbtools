# dbtools

A simple diagnostics tool for MongoDB databases.

## Introduction

dbtools is a small tool that simplifies the analysis of a MongoDB database and identifies inconsistencies in the documents in the database and the expected model. The main goal of the way the program is structured is to guarantee low memory usage, as loading a database's worth of logs in RAM at once could easily become a problem.

## Usage

### Dependencies

dbtools uses a few libraries, namely `pymongo`, `json`, `bson` and a few functions from `os` and `sys`. The only one that isn't included by default upon installing Python 3 is `pymongo`, so make sure you have that instlled (pip does the job, as usual).

### Model setup

Setting up the model is a relatively straight-forward process. This is how you'd go about creating the model for your first collection:

* Create an environment, giving it a name and a path where the .dbconf file will be saved

* Create a server, giving it a name and passing it the appropriate connection string

* Create a database, giving it a name (for the interface) and its name within the server (called the address)

* Create a collection, giving it a name (for the interface) and its name within the server (called the address)

* Create the properties contained in the document model for that collection

### Property types

There are a few types of properties that can be set up in dbtools. They are:

#### Simple properties

Simple one-value properties, optional or not, that can be of type `ObjectID`, `String`, `Number`, `Boolean` or `Any` (of these).

#### Array properties

Arrays of properties, optional or not, with all elements being a single type (same as simple properties).

#### Object properties

Object of properties, optional or not. Contains any number of named simple properties.

#### Controlled object properties

Same as object properties, but also contain a boolean controller property, which, if false, makes all other properties optional.

e.g.:

    active: {
      yes: Boolean,
      since: Number //timestamp
    }

### Analysis

Once your environment is set up, you can go to the environment view screen and enter the analysis screen with `(R) Run analysis`. There, you'll be able to select the target(s) for analysis by path and `(S) Select` and `(D) Deselect`. This should be pretty intuitive. Once done, you run the analysis, and wait. Your logs will be saved in `logs/`, relative to the path to `dbtools.py`.

#### Viewing analysis results

First, close your environment, and back in the analysis selection screen you go into `(L) Log viewer`, which will show you all analysis logs in the aforementioned `logs/` directory. You can navigate down to the collection level, where you'll be able to view a detailed summary of which properties in that collection have issues, and what types of issues, at that.

## Limitations

As of version 1.0.0, dbtools does not support nested objects as properties, nor does it support arrays of non-simple properties. I have plans to implement this in the future, but free time is too short for a too large number of projects. One day it'll be more complete in this sense.
