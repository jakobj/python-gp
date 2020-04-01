from .node import Node


class Primitives:
    """Class collecting primitives of the Cartesian Genetic Programming framework.
    """

    _n_primitives = 0
    _max_arity = 0
    _primitives = None

    def __init__(self, primitives):
        """Init function.

        Parameters
        ----------
        primitives : List[gp.CPGNode]
            List of primitives.
        """
        for i in range(len(primitives)):
            if not isinstance(primitives[i], type):
                raise TypeError(f"expected class but received {type(primitives[i])}")
            if not issubclass(primitives[i], Node):
                raise TypeError(f"expected subclass of Node but received {primitives[i].__name__}")

        self._n_primitives = len(primitives)

        self._primitives = {}
        for i in range(len(primitives)):
            self._primitives[i] = primitives[i]

        # hide primitives dict behind MappingProxyType to make sure it
        # is not changed after construction
        # unfortunately not supported by pickle, necessary for
        # multiprocessing; another way to implement this?
        # self._primitives = types.MappingProxyType(self._primitives)

        self._determine_max_arity()

    def _determine_max_arity(self):

        arity = 1  # minimal possible arity (output nodes need one input)

        for idx, p in self._primitives.items():
            if arity < p._arity:
                arity = p._arity

        self._max_arity = arity

    def sample(self, rng):
        """Sample a random primitive.

        Parameters
        ----------
        rng : numpy.RandomState
            Random number generator instance to use for crossover.

        Returns
        -------
        List[Tuple(str, gp.CPGNode)]
        """
        return rng.choice(self.alleles)

    def __getitem__(self, key):
        return self._primitives[key]

    @property
    def max_arity(self):
        return self._max_arity

    @property
    def alleles(self):
        return tuple(self._primitives.keys())

    def __len__(self):
        return len(self._primitives)