from neh import NEH
from cds import CDS
from johnson import JOHNSON
import commonFunction
import interface
import benchmark

def testFunction():
    print(" *********************************************\n",
          "Running Test Samples from Relavent Files\n",
          "********************************************* \n")
    n=NEH().test()
    cds = CDS()
    cds.test()
    JOHNSON().test()
    print(" *********************************************\n",
          "                       Ends\n",
          "********************************************* \n")
    
    
    
instanceid=13

# Reading Taillads Sample from Dataset 
instance = commonFunction.read_files()
nbm, nbj = instance[instanceid].shape
p_ij = instance[instanceid]
print(" *********************************************\n",
      "                       NEH                    \n",
      "********************************************* \n")
#Setting up NEH Class to run the ALGO 
n=NEH()
# Run n.test() will run the test case from file nehTest.txt
seq, cmax = n.nehAlgo(p_ij, nbm, nbj)
print("nbMachines:", nbm)
print("nbJobs:", nbj)
print("Taillads Instance No:",(instanceid+1))
print("Instance => \n",p_ij)
# print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
print("NEH: \n","MakeSpan :", cmax ," => Sequence ",seq)
# interface.graphic("NEH", seq, nbj, nbm, commonFunction.makespan(seq, p_ij, nbm), p_ij) # Show Graphs
print(" *********************************************\n",
      "                       CDS                    \n",
      "********************************************* \n")
# Setting up CDS class to run ALGO 
cds=CDS()
# Run n.test() will run the test case from file example2.txt
cdsseq, cdscmax = cds.cdsAlgo(p_ij, nbm, nbj)
# print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)
print("CDS: \n", "MakeSpan :", cdscmax, " => Sequence ", cdsseq)
print(" *********************************************\n",
      "                       JOHNSON                \n",
      "********************************************* \n")
# Setting up Jhonson class to run ALGO 
john=JOHNSON()
# Run n.test() will run the test case from file example.txt
johnseq, johncmax = john.johnsonAlgo(p_ij, nbm, nbj)
# print("data: p_ij, the processing time of jth job on ith machine\n", p_ij)

print("JOHNSON: \n", "MakeSpan :", johncmax, " => Sequence ", johnseq)

testFunction()
