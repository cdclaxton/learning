# Examples from https://goteleport.com/blog/z3-rbac/

import z3

# Define unbound string vatiables
user_country = z3.String("user_country")
node_location = z3.String("node_location")
node_running = z3.String("node_running")

# Access permitted if
# (node_location = user_country) ∧ (node_running = "app")
role1 = z3.And(user_country == node_location, node_running == z3.StringVal("app"))

solver = z3.Solver()
solver.add(role1)
result = solver.check()
if z3.sat == result:
    print(solver.model())
else:
    print("No solution")

# The result is:
#
# [node_running = "app",
#  node_location = "",
#  user_country = ""]
#
# This is a trivial set of values that satisfy the constraints.

# Access permitted if
# (node_location != user_country) ∧ (node_running = "app")
role2 = z3.And(user_country != node_location, node_running == z3.StringVal("app"))

# Are the two roles distinct?
solver = z3.Solver()
solver.add(z3.Distinct(role1, role2))
result = solver.check()
if z3.sat == result:
    print(solver.model())
else:
    print("No solution")

# The result is:
#
# [node_location = "",
#  user_country = "A",
#  node_running = "app"]
#
# and those values make the access distinct, i.e. role1 can't access the resouse
# but role2 can.

# Is access permitted for a specific set of values?
solver = z3.Solver()
solver.add(role1)
solver.add(user_country == "France")
solver.add(node_location == "France")
solver.add(node_running == "app")

if z3.sat == solver.check():
    print("Allowed")
else:
    print("Denied")

# The result is: Allowed
