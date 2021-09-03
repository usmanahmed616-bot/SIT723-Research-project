import commonFunction
import interface

#####################################################
# algorithm for neh
#####################################################

class NEH:
    def sum_processing_time(self,index_job, data, nb_machines):
        sum_p = 0
        for i in range(nb_machines):
            sum_p += data[i][index_job]
        return sum_p
    
    
    def order_neh(self,data, nb_machines, nb_jobs):
        my_seq = []
        for j in range(nb_jobs):
            my_seq.append(j)
        return sorted(my_seq, key=lambda x: self.sum_processing_time(x, data, nb_machines), reverse=True)
    
    
    def insertion(self,sequence, index_position, value):
        new_seq = sequence[:]
        new_seq.insert(index_position, value)
        return new_seq
    
    
    def nehAlgo(self,data, nb_machines, nb_jobs):
        order_seq = self.order_neh(data, nb_machines, nb_jobs)
        seq_current = [order_seq[0]]
        for i in range(1, nb_jobs):
            min_cmax = float("inf")
            for j in range(0, i + 1):
                tmp_seq = self.insertion(seq_current, j, order_seq[i])
                cmax_tmp = commonFunction.makespan(tmp_seq, data, nb_machines)[nb_machines - 1][len(tmp_seq)]
                # print(tmp_seq, cmax_tmp)
                if min_cmax > cmax_tmp:
                    best_seq = tmp_seq
                    min_cmax = cmax_tmp
            seq_current = best_seq
        # print(tmp_seq, cmax_tmp)
        return seq_current, commonFunction.makespan(seq_current, data, nb_machines)[nb_machines - 1][nb_jobs]
    def test(self):
        nbm, nbj, p_ij = commonFunction.read_from_file("nehTest.txt")
        seq, cmax = self.nehAlgo(p_ij, nbm, nbj)
        print("nbMachines:", nbm)
        print("nbJobs:", nbj)
        print("Instance => \n", p_ij)
        # print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
        print("NEH: \n", "MakeSpan :", cmax, " => Sequence ", seq)

# # run NEH
# nbm, nbj, p_ij = commonFunction.read_from_file("nehTest.txt")
# seq, cmax = neh(p_ij, nbm, nbj)
# print("nbMachines:", nbm)
# print("nbJobs:", nbj)
# print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
# print("neh:", seq, cmax)
# interface.graphic("NEH", seq, nbj, nbm, commonFunction.makespan(seq, p_ij, nbm), p_ij)
