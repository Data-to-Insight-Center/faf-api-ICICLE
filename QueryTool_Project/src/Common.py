from src.Data_Lookup import QueryTool, logger
import src.queries.faf_mapping as metrics
import src.queries.state_mapping as sm


class Common:
    """
    This class generates a query for all of the exports comming out of a particular location.
    origin(string): the location which can be in state or regional
    timeframe(list of int): this attrubute gives the timeframe of data being requested
    """

    def __init__(
            self,
            timeframe = [],
            flow="",
    ):

        self.query = "SELECT "
        self.table = None,
        self.timeframe = timeframe
        self.flow = flow



    def setup(self):

        self.table = self._checkLocations()
        if self.table == False: return False  # incorrect origin destination match
        # if not self._checkTimeframe(): return False  # incorrect times
        cols = []

        if self.table[:3] == "faf":
            cols.append(metrics.faf0["dms_orig"][0])
            cols.append(metrics.faf0["dms_dest"][0])
            cols.append(metrics.faf0["sctg2"][0])
            cols.append(metrics.faf0["dms_mode"][0])

        else:
            cols.append(sm.state0["dms_orig"][0])
            cols.append(sm.state0["dms_dest"][0])
            cols.append(sm.state0["sctg2"][0])
            cols.append(sm.state0["dms_mode"][0])

        if self.table[:3] == "faf":
            for year in [2017,2024]:
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
            self.query += metrics.faf0["dms_orig"][1] + " "
            self.query += metrics.faf0["dms_dest"][1] + " "
            self.query += metrics.faf0["sctg2"][1] + " "
            self.query += metrics.faf0["dms_mode"][1] + " "

        else:
            self.query += sm.state0["dms_orig"][1] + " "
            self.query += sm.state0["dms_dest"][1] + " "
            self.query += sm.state0["sctg2"][1] + " "
            self.query += sm.state0["dms_mode"][1] + " "

        # Checks for where statements
        where = "WHERE"

        if self.table == "faf0" or self.table == "faf1":
            self.query += f"{where} of0.description = '{self.origin}' "
            if self.destination:
                self.query += f" AND df.description = '{self.destination}' "

        if self.table == "state0" or self.table == "state1":
            self.query += f"{where} os.description = '{self.origin}' "
            if self.destination:
                self.query += f" AND ds.description = '{self.destination}' "

        if self.transpotation:
            self.query += f" AND m.description = '{self.transpotation}' "

        if self.commodity:
            self.query += f" AND c.description = '{self.commodity}' "

        self.query += ";"
        return self.query

    def mode_details(self):
        # self.timeframe = [2017,2024]
        # self.table = 'state1'
        self.query = "SELECT "
        self.table = 'state'
        if self.flow == "domestic":
            self.table += "1"
        elif self.flow == "foreign_import":
            self.table += "2"
        else:
            self.table += "3"

        if self.table == False: return False  # incorrect origin destination match
        # if not self._checkTimeframe(): return False  # incorrect times
        cols = []

        if self.table == "faf1":
            #     cols.append(metrics.faf0["dms_orig"][0])
            #     cols.append(metrics.faf0["dms_dest"][0])
            #     cols.append(metrics.faf0["sctg2"][0])
            cols.append(metrics.faf0["dms_mode"][0])
        #
        if  self.table == "state1":
            #     cols.append(sm.state0["dms_orig"][0])
            #     cols.append(sm.state0["dms_dest"][0])
            #     cols.append(sm.state0["sctg2"][0])
            cols.append(sm.state0["dms_mode"][0])


        if self.table == "faf2":
            # cols.append(metrics.faf2["fr_orig"][0])
            cols.append(metrics.faf2["fr_inmode"][0])

        if self.table == "faf3":
            # cols.append(metrics.faf3["fr_dest"][0])
            cols.append(metrics.faf3["fr_outmode"][0])

        if self.table == "state2":
            # cols.append(sm.state2["fr_orig"][0])
            cols.append(sm.state2["fr_inmode"][0])

        if self.table == "state3":
            # cols.append(sm.state3["fr_dest"][0])
            cols.append(sm.state3["fr_outmode"][0])

        if self.table[:3] == "faf":
            for year in self.timeframe:
                try:
                    cols.append(metrics.tons_sum[str(year)])
                except:
                    continue
            for year in self.timeframe:
                try:
                    cols.append(metrics.value_sum[str(year)])
                except:
                    continue
        else:
            for year in self.timeframe:
                try:
                    cols.append(sm.tons_sum[str(year)])
                except:
                    continue
            for year in self.timeframe:
                try:
                    cols.append(sm.value_sum[str(year)])
                except:
                    continue

        self.query += ", ".join(cols) + " "

        self.query += f"FROM {metrics.table[self.table]} "

        if self.table == "faf1":
            # self.query += metrics.faf0["dms_orig"][1] + " "
            # self.query += metrics.faf0["dms_dest"][1] + " "
            # self.query += metrics.faf0["sctg2"][1] + " "
            self.query += metrics.faf0["dms_mode"][1] + " "
            self.query += f" GROUP BY m.description "

        if self.table == "state1":

            # self.query += sm.state0["dms_orig"][1] + " "
            # self.query += sm.state0["dms_dest"][1] + " "
            # self.query += sm.state0["sctg2"][1] + " "
            self.query += sm.state0["dms_mode"][1] + " "
            self.query += f" GROUP BY m.description "

        if self.table== "faf2":

            self.query += metrics.faf2["fr_inmode"][1] + " "
            self.query += f" GROUP BY fom.description "

        if self.table== "faf3":

            self.query += metrics.faf3["fr_outmode"][1] + " "
            self.query += f" GROUP BY fdm.description "

        if self.table== "state2":

            self.query += sm.state2["fr_inmode"][1] + " "
            self.query += f" GROUP BY fom.description "

        if self.table == "state3":

            self.query += sm.state3["fr_outmode"][1] + " "
            self.query += f" GROUP BY fdm.description "



        # Checks for where statements
        # where = "WHERE"
        #
        # self.query += f" GROUP BY m.description "
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
        print(self.query)
        lookup = QueryTool()
        data = lookup.query(self.query)
        print(data)
        # start_year, end_year = self.timeframe[0], self.timeframe[1]
        start_year = self.timeframe[0]
        key_value_pairs = dict(zip(data["Transportation"], data[str(start_year)].round(2)))

        print(key_value_pairs)
        return key_value_pairs


    def bar_chart_details(self):
        # self.timeframe = [2017]
        self.table = 'state'
        if self.flow == "domestic":
            self.table += "1"
        elif self.flow == "foreign_import":
            self.table += "2"
        else:
            self.table += "3"

        # self.table = 'state2'
        self.query = "SELECT "
        if self.table == False: return False  # incorrect origin destination match
        # if not self._checkTimeframe(): return False  # incorrect times
        cols = []

        # if self.table[:3] == "faf":
            #     cols.append(metrics.faf0["dms_orig"][0])
            #     cols.append(metrics.faf0["dms_dest"][0])
            #     cols.append(metrics.faf0["sctg2"][0])
            # cols.append(metrics.faf0["dms_mode"][0])
        #
        # else:
            #     cols.append(sm.state0["dms_orig"][0])
            #     cols.append(sm.state0["dms_dest"][0])
            #     cols.append(sm.state0["sctg2"][0])
            # cols.append(sm.state0["dms_mode"][0])
        start_year, end_year = self.timeframe[0], self.timeframe[1]
        self.timeframe = list(range(start_year, end_year + 1))
        if self.table[:3] == "faf":
            for year in self.timeframe:
                try:
                    cols.append(metrics.tons_sum[str(year)])
                except:
                    continue
            # for year in self.timeframe:
            #     try:
            #         cols.append(metrics.value_sum[str(year)])
            #     except:
            #         continue
        else:
            for year in self.timeframe:
                try:
                    cols.append(sm.tons_sum[str(year)])
                except:
                    continue
            # for year in self.timeframe:
            #     try:
            #         cols.append(sm.value_sum[str(year)])
            #     except:
            #         continue

        self.query += ", ".join(cols) + " "

        self.query += f"FROM {metrics.table[self.table]} "

        # if self.table[:3] == "faf":
            # self.query += metrics.faf0["dms_orig"][1] + " "
            # self.query += metrics.faf0["dms_dest"][1] + " "
            # self.query += metrics.faf0["sctg2"][1] + " "
            # self.query += metrics.faf0["dms_mode"][1] + " "

        # else:
            # self.query += sm.state0["dms_orig"][1] + " "
            # self.query += sm.state0["dms_dest"][1] + " "
            # self.query += sm.state0["sctg2"][1] + " "
            # self.query += sm.state0["dms_mode"][1] + " "

        # Checks for where statements
        # where = "WHERE"
        #
        # self.query += f" GROUP BY m.description "
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
        return self.query

    def domestic_flow_tab(self):

        lookup = QueryTool()

        data_state_origin = lookup.query("SELECT description FROM d_faf;")
        result_state_origin = data_state_origin["description"].tolist()

        data_state_destination = lookup.query("SELECT description FROM d_faf;")
        result_state_destination= data_state_destination["description"].tolist()

        # Fetch the second query result
        data_com = lookup.query("SELECT description FROM c;")
        result_commodity = data_com["description"].tolist()

        data_domestic_mode = lookup.query("SELECT description FROM m;")
        result_domestic_mode = data_domestic_mode["description"].tolist()

        data_state_year = lookup.query("SELECT description FROM year_state;")
        result_state_year = data_state_year["description"].tolist()

        output = {"domestic_origin": result_state_origin,
                  "domestic_destination": result_state_destination,
                  "commodity": result_commodity,
                  "domestic_mode": result_domestic_mode,
                  "state_year": result_state_year
                  }
        return output

    def foreign_export_tab(self):

        lookup = QueryTool()

        data_domestic_origin = lookup.query("SELECT description FROM d_faf;")
        result_domestic_origin = data_domestic_origin["description"].tolist()

        data_foreign_destination = lookup.query("SELECT description FROM fd;")
        result_foreign_destination= data_foreign_destination["description"].tolist()

        # Fetch the second query result
        data_com = lookup.query("SELECT description FROM c;")
        result_commodity = data_com["description"].tolist()

        data_foreign_destination_mode = lookup.query("SELECT description FROM fdm;")
        result_foreign_destination_mode = data_foreign_destination_mode["description"].tolist()

        data_state_year = lookup.query("SELECT description FROM year_state;")
        result_state_year = data_state_year["description"].tolist()

        output = {"domestic_origin": result_domestic_origin,
                  "foreign_destination": result_foreign_destination,
                  "commodity": result_commodity,
                  "foreign_destination_mode": result_foreign_destination_mode,
                  "state_year": result_state_year
                  }
        return output

    def foreign_import_tab(self):

        lookup = QueryTool()

        data_foreign_origin = lookup.query("SELECT description FROM fo;")
        result_foreign_origin = data_foreign_origin["description"].tolist()

        data_domestic_destination = lookup.query("SELECT description FROM d_faf;")
        result_domestic_destination= data_domestic_destination["description"].tolist()

        # Fetch the second query result
        data_com = lookup.query("SELECT description FROM c;")
        result_commodity = data_com["description"].tolist()

        data_foreign_origin_mode = lookup.query("SELECT description FROM fom;")
        result_foreign_origin_mode = data_foreign_origin_mode["description"].tolist()

        data_state_year = lookup.query("SELECT description FROM year_state;")
        result_state_year = data_state_year["description"].tolist()

        output = {"foreign_origin": result_foreign_origin,
                  "domestic_destination": result_domestic_destination,
                  "commodity": result_commodity,
                  "foreign_origin_mode": result_foreign_origin_mode,
                  "state_year": result_state_year
                  }
        return output

    def _table(self):
        """
        Just impends the FROM command with the actual table name to the query
        """
        self.query += f"FROM {metrics.table[self.table]} "

    def _checkLocations(self):
        """Checks the locations and sets table based on origin and destination"""
        tool = QueryTool()
        ostate = tool.query("SELECT description FROM o_state;")
        ofaf = tool.query("SELECT description FROM o_faf;")
        fo = tool.query("SELECT description FROM fo;")
        # retrive the table
        if any(o == self.origin for o in ostate['description']):
            return 'state'

        if any(o == self.origin for o in ofaf['description']):
            return 'faf'

        # if any(o == self.origin for o in fo['description']):
        #    return 'state2'

        return False

    def _checkTimeframe(self):
        """
        Chcks to make sure the numbes of years in timeframe are not 0 or more than 2. Then if there are two years, this method populates the years inbetween
        """
        tf = self.timeframe
        if len(tf) > 2:
            return False
        elif len(tf) == 0:
            return False
        elif len(tf) == 2:
            self.timeframe = [x for x in range(tf[0], tf[1] + 1)]
        return True
