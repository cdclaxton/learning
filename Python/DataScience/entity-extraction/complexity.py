# Each entity only occupies one token. If there are N tokens and M entities, then
# a naive approch would require N * M equality checks.
#
# +----+----+----+
# | T0 | T1 | T2 |
# +----+----+----+
#
# Each token is checked against each of the M entities. If a set is used that
# has O(1) lookup complexity, then the complexity of the entity matching is
# O(N).
