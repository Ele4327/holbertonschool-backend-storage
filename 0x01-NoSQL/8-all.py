#!/usr/bin/env python3

"""
Write a Python function that lists all documents in a collection
"""
def list_all(mongo_collection):
    """list_all() Return an empty list if no document
    in the collection"""
    return(mongo_collection.find())
