import sys
END_OF_INPUT = 'EOF'
class Node:
    def __init__(self, name, start=False, accept=False, reject=False):
        self.start = start
        self.accept = accept
        self.reject = reject
        self.rules = {}
        self.name = name

    def __key(self):
        return self.name

    def __eq__(self, other):
        return (isinstance(other, self.__class__) 
                and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.__key()

def simulate(start, statemap, step=False):
    kb = None
    while True:
        kb = raw_input()
        cmts = kb.find('//')
        if cmts >= 0:
            kb = kb[0: cmts].strip()
        if not kb: continue
        if kb == END_OF_INPUT: return
        kb = list(kb)
        slen = len(kb)
        head = 0
        state = start
        badsym = False
        while(not (state.reject or state.accept)):
            value = state.rules.get(kb[head])
            if value == None:
                print "TM rejected on invalid symbol: " + kb[head]
                print "State: " + state.name
                print "Final string"
                print "------------"
                print ''.join(kb).rstrip('_')
                badsym = True
                break
            to, replace, hmove  = value
            kb[head] = replace
            if head + hmove < 0:
                head = 0
            elif head + hmove >= slen:
                kb.append('_')
                slen +=1
                head += hmove
            else:
                head += hmove
            if step:
                print "String: " + ''.join(kb)
                print "        " + " "*(head) + "^"
                print "H = {} (+ {})".format(head-hmove, hmove)
                print "[{}]-->[{}]".format(state.name, to.name)
                raw_input()
            state = to
        if not badsym:
            rejected = "rejected" if state.reject else ''
            accepted = "accepted" if state.accept else ''
            print "TM[{}] in state {}".format(rejected + accepted, state.name)
            print "Final string"
            print "------------"
            print ''.join(kb).rstrip('_')
            print ''.join(kb).rstrip('_').count('0')
    

def parse_states():
    """
        You must define a state 0 as the entry point into the system.
    """
    states = {}
    # 1. Read whether step debugging is on or not
    # STEP ON
    # STEP OFF
    stepping = raw_input()
    stepping = stepping[stepping.rfind("STEP")+4:].strip().lower()
    print stepping
    if stepping == 'on':
        stepping = True
    else:
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        stepping = False
    # 2. Read the names of all the states
    # 	 The following prefixes can be used to indicate the type of the edge
    #	 A - Accepting
    #	 R - Rejecting
    #	 S - Start state
    defs = raw_input().strip()
    defs = defs.split(",")
    start = None
    for i in defs:
        f = i[1:]
        if i.startswith('S'):
            start = Node(f, start=True)
            states[f] = start
        elif i.startswith('A'):
            states[f] = Node(f, accept=True)
        elif i.startswith('R'):
            states[f] = Node(f, reject=True)
        else:
            states[i] = Node(i)
    assert start
    while True:
        line = raw_input().strip()
        # Look for the end of input sentinel EOF
        if line == END_OF_INPUT:
            break
        cmts = line.find('//')
        if cmts >= 0:
            line = line[0: cmts].strip()
        if not line: continue
        l, r = [i.strip() for i in line.split(':', 1)]
        frm, to = [i.strip() for i in l.split('->', 1)]
        # Fetch the rule lists
        frules = states[frm].rules
        to     = states[to]
        # Fetch or create the specific rule set
        read, replace = [i.strip() for i in r.split('->',1)]
        replace, head = [i.strip() for i in replace.split(',')]
        head = head.lower()
        assert head == 'l' or head == 'r'
        head = 1 if head == 'r' else -1
        frules[read] = (to, replace, head)
    return stepping, start, states
if __name__ == "__main__":
    stepping, start, statemap = parse_states()
    simulate(start, statemap, stepping)
