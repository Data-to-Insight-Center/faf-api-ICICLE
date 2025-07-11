from src.Data_Lookup import QueryTool, logger
import src.queries.faf_mapping   as metrics
import src.queries.state_mapping as sm
class Exports:
    """
    This class generates a query for all of the exports comming out of a particular location.
    origin(string): the location which can be in state or regional
    timeframe(list of int): this attrubute gives the timeframe of data being requested
    """
    def __init__(
            self,
            origin    = "",
            timeframe = [],
            commodity = "",
            destination = "",
            transpotation="",
            flow="",

    ):

        self.query = "SELECT "

        self.origin    = origin
        self.table     = None
        self.timeframe = timeframe
        self.transpotation = transpotation
        self.commodity = commodity
        self.destination = destination
        self.flow = flow

    def setup(self):
        self.table = self._checkLocations()

        if self.flow == "domestic":
            self.table += "1"
        elif self.flow == "foreign_import":
            self.table += "2"
        else:
            self.table += "3"

        if self.table == False: return False        #incorrect origin destination match
        if not self._checkTimeframe(): return False #incorrect times
        cols = []

        if self.table == "faf1":
            cols.append(metrics.faf0["dms_orig"][0])
            cols.append(metrics.faf0["dms_dest"][0])
            cols.append(metrics.faf0["sctg2"][0])
            cols.append(metrics.faf0["dms_mode"][0])

        if self.table == "state1":

            cols.append(sm.state0["dms_orig"][0])
            cols.append(sm.state0["dms_dest"][0])
            cols.append(sm.state0["sctg2"][0])
            cols.append(sm.state0["dms_mode"][0])

        if self.table == "faf2":
            cols.append(metrics.faf2["fr_orig"][0])
            cols.append(metrics.faf2["fr_inmode"][0])
            cols.append(metrics.faf2["dms_dest"][0])
            cols.append(metrics.faf2["sctg2"][0])

        if self.table == "faf3":
            cols.append(metrics.faf3["fr_dest"][0])
            cols.append(metrics.faf3["fr_outmode"][0])
            cols.append(metrics.faf3["dms_orig"][0])
            cols.append(metrics.faf3["sctg2"][0])

        if self.table == "state2":
            cols.append(sm.state2["fr_orig"][0])
            cols.append(sm.state2["fr_inmode"][0])

        if self.table == "state3":
            cols.append(sm.state3["fr_dest"][0])
            cols.append(sm.state3["fr_outmode"][0])
            cols.append(sm.state0["dms_orig"][0])
            cols.append(sm.state0["sctg2"][0])
 
        if self.table[:3] == "faf":
            for year in self.timeframe:
                try: cols.append(metrics.tons[str(year)])
                except: continue
            for year in self.timeframe:
                try: cols.append(metrics.value[str(year)])
                except: continue
        else:
             for year in self.timeframe:
                try: cols.append(sm.tons[str(year)])
                except: continue
             for year in self.timeframe:
                try: cols.append(sm.value[str(year)])
                except: continue

        self.query += ", ".join(cols) + " "

        self._table()

        if self.table == "faf1":
            self.query += metrics.faf0["dms_orig"][1] + " "
            self.query += metrics.faf0["dms_dest"][1] + " "
            self.query += metrics.faf0["sctg2"][1] + " "
            self.query += metrics.faf0["dms_mode"][1] + " "

        if self.table == "state1":

            self.query += sm.state0["dms_orig"][1] + " "
            self.query += sm.state0["dms_dest"][1] + " "
            self.query += sm.state0["sctg2"][1] + " "
            self.query += sm.state0["dms_mode"][1] + " "

        if self.table == "faf2":
            self.query += metrics.faf2["fr_orig"][1] + " "
            self.query += metrics.faf2["fr_inmode"][1] + " "
            self.query += metrics.faf2["dms_dest"][1] + " "
            self.query += metrics.faf2["sctg2"][1] + " "

        if self.table== "faf3":
            self.query += metrics.faf3["dms_orig"][1] + " "
            self.query += metrics.faf3["fr_dest"][1] + " "
            self.query += metrics.faf3["fr_outmode"][1] + " "
            self.query += metrics.faf3["sctg2"][1] + " "

        if self.table == "state2":
            self.query += sm.state2["fr_orig"][1] + " "
            self.query += sm.state2["fr_inmode"][1] + " "
            self.query += sm.state0["dms_dest"][1] + " "
            self.query += sm.state0["sctg2"][1] + " "

        if self.table == "state3":
            self.query += sm.state3["fr_dest"][1] + " "
            self.query += sm.state3["fr_outmode"][1] + " "
            self.query += sm.state0["dms_orig"][1] + " "
            self.query += sm.state0["sctg2"][1] + " "


        #Checks for where statements
        where = "WHERE"

        if self.table == "faf0" or self.table == "faf1":
            if self.origin:
                self.query += f"{where} of0.description = '{self.origin}' "
            if self.destination:
                self.query += f" AND df.description = '{self.destination}' "
            if self.transpotation:
                self.query += f" AND m.description = '{self.transpotation}' "

        if self.table == "faf2":
            if self.origin:
                self.query += f"{where} fo.description = '{self.origin}' "
            if self.destination:
                self.query += f" AND df.description = '{self.destination}' "
            if self.transpotation:
                self.query += f" AND fom.description = '{self.transpotation}' "

        if self.table == "state0" or self.table == "state1":
            if self.origin:
                self.query += f"{where} os.description = '{self.origin}' "
            if self.destination and self.origin:
                self.query += f" AND ds.description = '{self.destination}' "
            if self.destination and (self.origin is None or self.origin == ""):
                self.query += f" WHERE ds.description = '{self.destination}' "
            if self.transpotation:
                self.query += f" AND m.description = '{self.transpotation}' "

        if self.table == "faf3" :
            if self.destination:
                self.query += f"{where} fd.description = '{self.destination}' "
            if self.origin:
                self.query += f" AND of0.description = '{self.origin}' "
            if self.transpotation:
                self.query += f" AND fdm.description = '{self.transpotation}' "

        if self.table == "state3":
            if self.destination:
                self.query += f"{where} fd.description = '{self.destination}' "
            if self.origin:
                self.query += f" AND os.description = '{self.origin}' "
            if self.transpotation:
                self.query += f" AND fdm.description = '{self.transpotation}' "

        if self.table == "state2":
            if self.origin:
                self.query += f"{where} fo.description = '{self.origin}' "
            if self.destination:
                self.query += f" AND ds.description = '{self.destination}' "


        if self.commodity:
            self.query += f" AND c.description = '{self.commodity}' "

        self.query += ";"
        logger.debug(self.query)
        return self.query

    def mode_details(self):
        self.table = self._checkLocations()
        if self.table == False: return False  # incorrect origin destination match
        if not self._checkTimeframe(): return False  # incorrect times
        cols = []

        if self.table[:3] == "faf":
        #     cols.append(metrics.faf0["dms_orig"][0])
        #     cols.append(metrics.faf0["dms_dest"][0])
        #     cols.append(metrics.faf0["sctg2"][0])
            cols.append(metrics.faf0["dms_mode"][0])
        #
        else:
        #     cols.append(sm.state0["dms_orig"][0])
        #     cols.append(sm.state0["dms_dest"][0])
        #     cols.append(sm.state0["sctg2"][0])
            cols.append(sm.state0["dms_mode"][0])

        if self.table[:3] == "faf":
            for year in self.timeframe:
                try:
                    cols.append(metrics.tons[str(year)])
                except:
                    continue
            for year in self.timeframe:
                try:
                    cols.append(metrics.value[str(year)])
                except:
                    continue
        else:
            for year in self.timeframe:
                try:
                    cols.append(sm.tons[str(year)])
                except:
                    continue
            for year in self.timeframe:
                try:
                    cols.append(sm.value[str(year)])
                except:
                    continue

        self.query += ", ".join(cols) + " "

        self._table()

        if self.table[:3] == "faf":
            # self.query += metrics.faf0["dms_orig"][1] + " "
            # self.query += metrics.faf0["dms_dest"][1] + " "
            # self.query += metrics.faf0["sctg2"][1] + " "
            self.query += metrics.faf0["dms_mode"][1] + " "

        else:
            # self.query += sm.state0["dms_orig"][1] + " "
            # self.query += sm.state0["dms_dest"][1] + " "
            # self.query += sm.state0["sctg2"][1] + " "
            self.query += sm.state0["dms_mode"][1] + " "

        # Checks for where statements
        # where = "WHERE"
        #
        # if self.table == "faf0" or self.table == "faf1":
        #     self.query += f"{where} of0.description = '{self.origin}' "
        #     if self.destination:
        #         self.query += f" AND df.description = '{self.destination}' "
        #
        # if self.table == "state0" or self.table == "state1":
        #     self.query += f"{where} os.description = '{self.origin}' "
        #     if self.destination:
        #         self.query += f" AND ds.description = '{self.destination}' "
        #
        # if self.transpotation:
        #     self.query += f" AND m.description = '{self.transpotation}' "
        #
        # if self.commodity:
        #     self.query += f" AND c.description = '{self.commodity}' "

        self.query += ";"
        logger.debug(self.query)
        return self.query



    def _table(self):
        """
        Just impends the FROM command with the actual table name to the query
        """
        self.query += f"FROM {metrics.table[self.table]} "

    def _checkLocations(self):
        """Checks the locations and sets table based on origin and destination""" 
        tool = QueryTool()
        ostate = tool.query("SELECT description FROM o_state;")
        ofaf   = tool.query("SELECT description FROM o_faf;")
        dfaf = tool.query("SELECT description FROM d_faf;")
        fo     = tool.query("SELECT description FROM fo;")
        #retrive the table
        if any(o == self.origin for o in ostate['description']):
            return 'state'

        if any(o == self.origin for o in ofaf['description']):
            return 'faf'
        if any(o == self.destination for o in ostate['description']):
            return 'state'
        if any(o == self.destination for o in dfaf['description']):
            return 'faf'
        if any(o == self.origin for o in fo['description']):
           return 'faf'

        return False

    def _checkTimeframe(self):        
        """
        Chcks to make sure the numbes of years in timeframe are not 0 or more than 2. Then if there are two years, this method populates the years inbetween
        """
        tf = self.timeframe
        if   len(tf) > 2:  return False
        elif len(tf) == 0: return False
        elif len(tf) == 2: self.timeframe = [x for x in range(tf[0], tf[1]+1)]
        return True
