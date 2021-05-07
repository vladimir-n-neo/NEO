"""A database encapsulating collections of near-Earth objects and their
close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
"""
A function will be made which makes it possible to link together the neos and
close approaches which we have been provided through the load_neos and
load_approaches. The parameters will be the neos and approaches itself.
This is our helper function for linking which we will use for the other
functions in database.py as well.
"""


def link_neos_and_approaches(neos, approaches):
    neosList = {}           # for the neos list
    approachesList = []    # for the approaches list

    # every close approach has attributes with designation and so does
    # every neo. We'll check if they match, then it will be linked.
    # Also, it will searched as well in the list we are making. If it
    # is already there, the approach will be appended to the neosList
    # in the approaches. Else, it will be given with a new neo.

    for approach in approaches:
        for neo in neos:
            if neo.designation == approach._designation:
                approach.neo = neo
                if neo.designation in neosList:
                    neosList[neo.designation].approaches.append(approach)
                else:
                    neo.approaches.append(approach)
                    neosList[neo.designation] = neo
                break
        approachesList.append(approach)

    for neo in neos:
        if neo.designation not in neosList:
            neosList[neo.designation] = neo

    return neosList.values(), approachesList


class NEODatabase:

    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):

        """Create a new `NEODatabase`.
        As a precondition, this constructor assumes that the collections
        of NEOs and close approaches haven't yet been linked - that is,
        the `.approaches` attribute of each `NearEarthObject` resolves
        to an empty collection, and the `.neo` attribute of each
        `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link
        them together - after it's done, the `.approaches` attribute of each
        NEO has a collection of that NEO's close approaches, and the `.neo`
        attribute of each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """

        self.neos_name = {}
        self.neos_designation = {}

        # this will save the values securely
        self._neos, self._approaches = link_neos_and_approaches(neos,
                                                                approaches)
        for neo in self._neos:
            if neo.name:
                self.neos_name[neo.name] = neo
            self.neos_designation[neo.designation] = neo

    def get_neo_by_designation(self, designation):

        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation,
        or `None`.
        """

        return self.neos_designation.get(designation)

    def get_neo_by_name(self, name):

        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """

        if name in self.neos_name:
            return self.neos_name[name]
        return None

    def query(self, filters=()):

        """Query close approaches to generate those that match a collection
        of filters.

        This generates a stream of `CloseApproach` objects that match all
        of the provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which
        isn't guaranteed to be sorted meaningfully, although is often sorted
        by time.

        :param filters: A collection of filters capturing user-specified
        criteria.
        :return: A stream of matching `CloseApproach` objects.
        """

        for approach in self._approaches:
            # map(func, iter) will be used to filter out the approaches
            # for CloseApproach objects.
            flag = False in map(lambda i: i(approach), filters)
            if flag is False:
                yield approach
