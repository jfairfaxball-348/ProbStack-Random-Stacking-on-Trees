module

public import TreeStack.Basic
public import TreeStack.Transfer
public import TreeStack.Branch
public import TreeStack.Message
public import TreeStack.PebblingMove
public import TreeStack.RootScore

public section

namespace ProbStack

theorem empty_ne_some_zero : Ne TreeStack.EMPTY (some 0) :=
  TreeStack.empty_ne_integer_zero

end ProbStack
