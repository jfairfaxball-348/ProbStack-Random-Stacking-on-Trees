import TreeStack.Basic
import TreeStack.Transfer
import TreeStack.Branch
import TreeStack.Message
import TreeStack.PebblingMove
import TreeStack.RootScore

namespace ProbStack

theorem empty_ne_some_zero : Ne TreeStack.EMPTY (some 0) :=
  TreeStack.empty_ne_integer_zero

end ProbStack
