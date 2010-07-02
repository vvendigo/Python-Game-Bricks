


class MarkovGenerator:

    def __init__(self, data, order=2):
        self.iteration = 0
        self.order = order
        self.data = {}
        self.ending = {}
        for item in data:
            for i in xrange(len(item)-order-1):
                key = item[i:i+order]
                val = item[i+order]
                if self.data.has_key(key):
                    self.data[key].add(val)
                else:
                    self.data[key] = set([val])
            key = item[-2]
            val = item[-1]
            if self.ending.has_key(key):
                self.ending[key].add(val)
            else:
                self.ending[key] = set([val])
        #endfor
        for k, v in self.data.items():
            self.data[k] = list(v)
        for k, v in self.ending.items():
            self.ending[k] = list(v)
    #end ef

    def generate(self, maxLen):
        i = self.iteration
        out = self.data.keys()[i%len(self.data)]
        try:
            while len(out) < maxLen - 1:
                out += self.data[out[-self.order:]][i%len(self.data[out[-self.order:]])]
                #i += 1
        except KeyError:
            pass

        try:
            out += self.ending[out[-1]][i%len(self.ending[out[-1]])]
            #print '!!', out
        except KeyError:
            pass

        self.iteration += 1
        return out
    #enddef

#endclass


data = ['aklabeth','brabenec','citus','deges','emanek','filuta','gymnazian',
        'hrubec','ilonka','jenicek','kulma','liptakov','manana','natalie',
        'otesanek','prdelnik','quido','raskolnikov','satanas','trabant',
        'ulicnik','vegetak','wendigo','xaver','ypsylon','zabacek']

gen = MarkovGenerator(data)

print gen.data
print gen.ending

for i in xrange(40):
    print gen.generate(8)

