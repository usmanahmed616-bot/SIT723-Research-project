import commonFunction

class JOHNSON:
    def johnsonAlgo(self,data, nb_machines, nb_jobs):
        seq_current = commonFunction.u(data, nb_jobs) + commonFunction.v(data, nb_jobs)
        return seq_current, commonFunction.makespan(seq_current, data, nb_machines)[nb_machines - 1][nb_jobs]

    def test(self):
        nbm, nbj, p_ij = commonFunction.read_from_file("johnsonTest.txt")
        seq, cmax = self.johnsonAlgo(p_ij, nbm, nbj)
        print("nbMachines:", nbm)
        print("nbJobs:", nbj)
        print("Instance => \n", p_ij)
        # print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
        print("JOHNSON: \n", "MakeSpan :", cmax, " => Sequence ", seq)
        # print("johnson:", seq, cmax)
        # interface.graphic("Johnson", seq, nbj, nbm, commonFunction.makespan(seq, p_ij, nbm), p_ij)

# run Johnson
# nbm, nbj, p_ij = commonFunction.read_from_file("example.txt")
# seq, cmax = johnson(p_ij, nbm, nbj)
# print("nbMachines:", nbm)
# print("nbJobs:", nbj)
# print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
# print("johnson:", seq, cmax)
# interface.graphic("Johnson", seq, nbj, nbm, commonFunction.makespan(seq, p_ij, nbm), p_ij)
