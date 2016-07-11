import ConfigParser
   
    
class configuration(object):
    def __init__(self, file):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read("odc.conf")
        

    def ConfigSectionMap(self,section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1