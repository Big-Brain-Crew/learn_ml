class JsonGenerator(object):
    def __init__(self, out_file):
        
        self.out_file = out_file
        self.out = open(self.out_file, "w+")

        self.root = {}
        self.index = self.root
    
    def _close(self):
        self.out.close()
        
    def indent(self, name):
        self.index = self.root[name]

    def unindent(self):
        self.index = self.root

    def add_entry(self, name, entry):
        if name in self.index and isinstance(self.index[name], list):
            self.index[name].append(entry)
        else:
            self.index[name] = entry
    
    def write(self):
        json.dump(self.root, self.out, indent=4)
        self._close()
        print("Saved to {}".format(self.out_file))