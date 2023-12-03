from abc import ABC, ABCMeta, abstractmethod


class Permutation(metaclass=ABCMeta):
    Field = None
    MATRIX = None

    @classmethod
    def get_state(self):
        pass

    @classmethod
    def get_state_size(self):
        pass

    @classmethod
    def apply_permutation(self):
        pass


class Poseidon(Permutation, metaclass=ABCMeta):
    ALPHA = None
    NB_FULL_ROUND = None
    NB_PARTIAL_ROUND = None
    ROUND_CONSTANTS = None
    STATE_SIZE = None

    # state is an array
    def __init__(self, state):
        # Verify the instance has all parameters set
        assert self.ALPHA is not None
        assert self.MATRIX is not None
        assert self.Field is not None
        assert self.STATE_SIZE is not None
        assert self.NB_FULL_ROUND is not None
        assert self.NB_PARTIAL_ROUND is not None
        assert self.ROUND_CONSTANTS is not None
        assert len(state) == self.STATE_SIZE
        self.state = state
        self.offset = 0

    def get_state_size(self):
        return self.STATE_SIZE

    def get_state(self):
        return [s.copy() for s in self.state]

    def apply_linear_layer(self):
        new_state = [self.Field.zero() for _ in range(self.STATE_SIZE)]
        for i in range(self.STATE_SIZE):
            for j in range(self.STATE_SIZE):
                new_state[i] += self.state[j] * self.MATRIX[i][j]
        self.state = new_state

    def add_round_constants(self):
        for i in range(self.STATE_SIZE):
            self.state[i] += self.ROUND_CONSTANTS[self.offset]
            self.offset += 1

    def apply_permutation(self):
        for i in range(self.NB_FULL_ROUND // 2):
            self.add_round_constants()
            for j in range(self.STATE_SIZE):
                self.state[j] = self.state[j].pow(self.ALPHA)
            self.apply_linear_layer()

        for i in range(self.NB_PARTIAL_ROUND):
            self.add_round_constants()
            self.state[0] = self.state[0].pow(self.ALPHA)
            self.apply_linear_layer()

        for i in range(self.NB_FULL_ROUND // 2):
            self.add_round_constants()
            for j in range(self.STATE_SIZE):
                self.state[j] = self.state[j].pow(self.ALPHA)
            self.apply_linear_layer()
