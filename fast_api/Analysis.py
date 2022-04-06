# import os
import re
import itertools
import json


class DynamicProgramAnalysis():

    def __init__(self, Script):

        self.__lines = Script.splitlines()
        # print(self.__lines)
        self.__Exception_Stack = []
        self.__Debug = False
        self.__unmonitored_outputs = []
        self.CELL_LENGTH = 20

    def Run(self, Debug=False):

        self.__Debug = Debug

        MESSAGE = f" Phase I - Extract_Variables "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        self.__Extract_Variables()

        MESSAGE = f" Phase II - Extract_Ranges "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        self.__Extract_Ranges()

        MESSAGE = f" Phase III - Build_CodeLines "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        self.__Build_CodeLines()

        MESSAGE = f" Phase IV - Build_Combinations "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        self.__Build_Combinations()

        MESSAGE = f" Phase V - Run_Iterations "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        self.__Run_Iterations()

        MESSAGE = f" Phase VI - Return_Values "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")
        ResultAsJson = self.__Return_Values()
        MESSAGE = f" XXX "
        if(self.__Debug):
            print("\n"+MESSAGE.center(82, '#')+"\n")

        return ResultAsJson

    def __Extract_Variables(self):

        self.__Var_IN = []
        self.__Var_OUT = []
        regex = r"([a-zA-Z]+)"
        for i in range(len(self.__lines)):
            exp = re.split('[{}; ]', self.__lines[i])
            Vars = [exp[x] for x in range(0, len(exp)) if (
                re.match('.*[a-zA-Z].*', exp[x]) != None)]
            for var in Vars:
                if(self.__lines[i].find(var) > self.__lines[i].find('=')):
                    if(self.__lines[i][self.__lines[i].find(var)+len(var)] == "{"):
                        self.__Var_IN.append(var)
                    else:
                        if(var not in (self.__Var_IN + self.__Var_OUT + self.__unmonitored_outputs)):
                            print("uncontrolled inputs :", var)
                elif(self.__lines[i].find(var) < self.__lines[i].find('=')):
                    if(var[0] == "[") and (var[len(var)-1] == "]"):
                        self.__Var_OUT.append(var[1:-1])
                    else:
                        self.__unmonitored_outputs.append(var)
                else:
                    print("unsatisfied variables :", var)
        Var_List = self.__Var_IN+self.__Var_OUT
        self.CELL_LENGTH = len(max(Var_List, key=len))+10
        if(self.__Debug):
            print(f"input_vars : {self.__Var_IN}")
            print(f"output_vars : {self.__Var_OUT}")

    def __Extract_Ranges(self):

        self.__Ranges = {}
        for i in range(len(self.__lines)):
            for var in self.__Var_IN:
                if(var in self.__lines[i]):
                    strt_idx = self.__lines[i].find(var)+len(var)
                    if(strt_idx != -1) and (self.__lines[i][strt_idx] == "{"):
                        end_idx = self.__lines[i][strt_idx:len(
                            self.__lines[i])].find("}")
                        ranges = self.__lines[i][(
                            strt_idx+1):((strt_idx + end_idx)-1)]
                        if(ranges.find(',') != -1):
                            sub = re.split(',', ranges)
                            st = float(sub[0])
                            nd = float(sub[1])
                            self.__Ranges[var] = self.__worst_case_in(st, nd)
                        else:
                            print("no comma found !")
                    else:
                        pass
        if(self.__Debug):
            print(f"ranges : {self.__Ranges}")

    def __Build_CodeLines(self):

        self.__CodeLines = ""
        code_lines_list = self.__lines.copy()
        for i in range(len(self.__lines)):
            for var in self.__Var_OUT:
                if var in code_lines_list[i]:
                    code_lines_list[i] = code_lines_list[i].replace(
                        "["+var+"]", "globals()[\""+var+"\"]")
        code_lines = "".join(code_lines_list.copy())
        func_calls = [code_lines[m.start(0):m.end(0)] for m in re.finditer(
            "{ *(?:(?!}).)*}", code_lines)]
        for x in func_calls:
            code_lines = code_lines.replace(x, "")
        self.__CodeLines = code_lines
        if(self.__Debug):
            print(self.__CodeLines)

    def __Build_Combinations(self):

        self.__Keyss = []
        self.__Combinations = []
        self.__Keyss = [x for x in self.__Ranges.keys()]
        valuess = [self.__Ranges[x] for x in self.__Ranges.keys()]
        self.__Combinations = [p for p in itertools.product(*valuess)]
        if(self.__Debug):
            print(self.__Combinations)

    def __Run_Iterations(self):

        for var in self.__Var_OUT:
            globals()[var+"_max"] = -10000000
            globals()[var+"_min"] = 10000000
        for combination in self.__Combinations:
            for x in range(len(self.__Keyss)):
                globals()[self.__Keyss[x]] = list(combination)[x]
            try:
                exec(self.__CodeLines)
                for x in range(len(self.__Var_OUT)):

                    if(globals()[self.__Var_OUT[x]] < globals()[self.__Var_OUT[x]+"_min"]):
                        globals()[self.__Var_OUT[x] +
                                  "_min"] = globals()[self.__Var_OUT[x]]
                        for y in range(len(self.__Keyss)):
                            globals()[self.__Var_OUT[x]+"_min" +
                                      self.__Keyss[y]] = globals()[self.__Keyss[y]]

                    if(globals()[self.__Var_OUT[x]] > globals()[self.__Var_OUT[x]+"_max"]):
                        globals()[self.__Var_OUT[x] +
                                  "_max"] = globals()[self.__Var_OUT[x]]
                        for y in range(len(self.__Keyss)):
                            globals()[self.__Var_OUT[x]+"_max" +
                                      self.__Keyss[y]] = globals()[self.__Keyss[y]]
            except Exception as ex:
                print(ex)
                if(str(x) not in self.__Exception_Stack):
                    self.__Exception_Stack.append(str(ex))
        if(self.__Debug):
            for var in self.__Var_OUT:
                output = "min("+var+"): "+str(globals()
                                              [var+"_min"]), "max("+var+"): "+str(globals()[var+"_max"])
                print(str(output))

    def __Return_Values(self):

        self.__Reports = {}
        if(self.__Exception_Stack == []):
            OUT = []
            for var in self.__Var_OUT:
                IN = []
                for y in range(len(self.__Keyss)):
                    IN.append({
                        "VAR": self.__Keyss[y],
                        "MAX": globals()[var+"_max"+self.__Keyss[y]],
                        "MIN": globals()[var+"_min"+self.__Keyss[y]]
                    })
                OUT.append({
                    "VAR": var,
                    "MAX": globals()[var+"_max"],
                    "MIN": globals()[var+"_min"],
                    "IN": IN
                })
            self.__Reports["OUT"] = OUT
        else:
            print("\n".join(self.__Exception_Stack))
        if(self.__Debug):
            print(self.__Reports)
        return self.__Reports

    def __abs_min_max(self, st, nd):

        lst = [st, nd]
        return [min(lst), max(lst)]

    def __act_min_max(self, st, nd):

        lst = [st, nd]
        return self.__abs_min_max(0, max(lst)) + [st]

    def __worst_case_in(self, st, nd):

        if((int(st) >= 0) and (int(nd) >= 0)):
            lst = self.__abs_min_max(st, nd)
        else:
            lst = self.__act_min_max(st, nd)

        return sorted(lst)


if __name__ == '__main__':

    SEA_script = """[P] = p{-10.0, 70.0} + r{-50.0, 50.0} * t{0.0, 0.20};
[Q] = q{-20.0, 20.0} + s{-50.0, 50.0} * t;
[R] = r;
[S] = s;"""

    result = DynamicProgramAnalysis(SEA_script).Run(Debug=False)
    print(json.dumps(result, indent=4))
