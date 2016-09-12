import lx


def query_User_Value(self, index, argPrefix, argName):
    if not self.dyna_IsSet(index):
        return lx.eval('user.value %s ?' % (argPrefix + argName))



def query_User_Values(self, argPrefix):
    userValues = []

    for i in xrange(0, self.attr_Count()):
        userValues.append(query_User_Value(self, i, argPrefix, self.attr_Name(i)))

    return userValues