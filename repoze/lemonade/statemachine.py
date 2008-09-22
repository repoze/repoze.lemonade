""" Finite state machine, useful for workflow-like features, based on
Skip Montanaro's FSM from
http://wiki.python.org/moin/FiniteStateMachine (ancient but simple #
and useful!)"""

from persistent import Persistent

_marker = ()

class StateMachineError(Exception):
    """ Invalid input to finite state machine"""

class StateMachine(Persistent):
    """ Persistent finite state machine featuring transition actions.

    The class stores a dictionary of (state, action) keys,
    and (state, transition) values.

    When a (state, action) search is performed:
    * an exact match is checked first,
    * (state, None) is checked next.

    The action is of the following form:
    * function(current_state, new_state, action, context)
    """

    def __init__(self, state_attr, initial_state=None):
        self.states = {}
        self.state_attr = state_attr
        self.initial_state = initial_state

    def add(self, state, action, newstate, transition_fn):
        """Add a transition to the FSM."""
        self.states[(state, action)] = (newstate, transition_fn)
        self._p_changed = True

    def execute(self, context, action):
        """Perform a transition and execute an action."""
        state = getattr(context, self.state_attr, _marker) 
        if state is _marker:
            state = self.initial_state
        si = (state, action)
        sn = (state, None)
        newstate = None
        # exact state match?
        if si in self.states:
            newstate, transition_fn = self.states[si]
        # no exact match, how about a None (catch-all) match?
        elif sn in self.states:
            newstate, transition_fn = self.states[sn]
        if newstate is None:
            raise StateMachineError(
                'No transition from %r using action %r' % (state, action))
        transition_fn(state, newstate, action, context)
        setattr(context, self.state_attr, newstate)

    def state_of(self, context):
        state = getattr(context, self.state_attr, self.initial_state)
        return state

    def actions(self, context, from_state=None):
        if from_state is None:
            from_state = self.state_of(context)
        actions = []
        for (state, action) in self.states.keys():
            if state == from_state:
                if action is not None:
                    actions.append(action)
        return actions
    
                
