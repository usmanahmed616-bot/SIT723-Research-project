#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from functools import lru_cache
from itertools import permutations
from random import randint, shuffle
from neh import NEH
import numpy as np
import commonFunction
import interface
from geneticFunctions import *

debug=False
class Flowshop(object):
    """
    A class for initiaizing & solving a Permutation Flowshop Scheduling Problem
    """

    def __init__(self, data=None, nb_machines=2, nb_jobs=6):
        """[summary]

        Keyword Arguments:
            data {list} -- A 2D array of processing time on machines (default: {None})
            nb_machines {int} -- Number of machines for the given problem must be the number of rows of first param (default: {2})
            nb_jobs {[type]} -- Number of jobs for the given problem, must be equal to the number of columns of the data param. (default: {6})
        """

        self.nb_machines = nb_machines
        self.nb_jobs = nb_jobs
        self.data = data


  
    def swapTwoJobs(self,seq,pos1,pos2):
        seq[pos1], seq[pos2] = seq[pos2], seq[pos1]
        return seq

    def generateRandomSequence(self):
        indexes = np.array([i for i in range(0,self.nb_jobs)])
    
        random.shuffle(indexes)
        print("Initial Solution",indexes)
        return indexes.tolist()
    def simulated_annealing(self,Ti = 10000,Tf = 1 ,alpha = 0.90):
        #Number of jobs given
        n = self.nb_jobs
        default_timer = None
        if sys.platform == "win32":
            default_timer = time.clock
        else:
            default_timer = time.time
        s = default_timer.__call__()
        neh=NEH()
        #Initialize the primary seq
        # old_seq,schedules,old_makeSpan, _ = self.palmer_heuristic()
        # old_seq, schedules, old_makeSpan, _ = n.nehAlgo(self.data, self.nb_machines, self.nb_jobs)
        old_seq,  old_makeSpan = neh.nehAlgo(
            self.data, self.nb_machines, self.nb_jobs)
        print('Initial Sequence of NEH =>', old_seq)
        print('Initial Sequence of NEH makespan =>', old_makeSpan)
        # old_seq=self.generateRandomSequence()
        # old_makeSpan = commonFunction.makespan(old_seq, self.data, self.nb_machines)[
        #         self.nb_machines - 1][len(old_seq)]
        if debug:
            print('Initial Sequence =>', old_seq)
            print('Initial Sequence makespan =>', old_makeSpan)
        bestSolution = old_makeSpan
        bestSequence = old_seq
        new_seq = []       
        delta_mk1 = 0
        #Initialize the temperature
        if debug:
            print("Initial Temperature =>",Ti)
            print("Final Temperature =>",Tf)
            print("Alpha",alpha)
        T = Ti
        Tf = Tf
        alpha = alpha
        # of iterations
        temp_cycle = 0
        
        while T >= Tf  :
            new_seq = old_seq.copy()
            # Insertion method
            # job = new_seq.pop(randint(0,n-1))
            # new_seq.insert(randint(0,n-1),job) # Swap and insertion for new sequence 
            
            #Swap Method
            u,v=randint(0, n-1), randint(0, n-1)
            job=u
            new_seq=self.swapTwoJobs(new_seq,u,v)
            
            new_make_span = commonFunction.makespan(new_seq, self.data, self.nb_machines)[
                self.nb_machines - 1][len(new_seq)]
            # new_make_span = self._get_makespan(new_seq,self.data)
            if debug:
                print('Job :',job)
                print('New Sequence :', new_seq)
                print('New Sequence make span:', new_make_span)
            delta_mk1 = new_make_span - old_makeSpan
            # if delta_mk1 <= 0:
            #     old_seq = new_seq
            #     old_makeSpan = new_make_span
            r=(old_seq == new_seq)
            if debug:
                print('Check Sequence Change',r)
            if r == False:
                if new_make_span < old_makeSpan:
                    if debug:
                        print("MakeSpan Swap Sequence", "new_make_span =>",new_make_span," old_makeSpan=>",old_makeSpan)
                    old_seq = new_seq
                    old_makeSpan = new_make_span
                    
                else :
                    delta_mk1 = new_make_span - old_makeSpan
                    Aprob = np.exp((-1*(delta_mk1)/T))
                    p = np.random.uniform(0.1,0.9)
                    if debug:
                        print("Proability",p)
                        print("Delta Change ", delta_mk1)
                        print("Aprob => ", Aprob)
                        print(p <= Aprob)
                    if p < Aprob:
                        old_seq = new_seq
                        old_makeSpan = new_make_span
                        if debug:
                         print("Proability Swap Sequence")
                    else :
                        #The solution is discarded
                        if debug:
                            print("Discard Iteration")
                            print('Old Sequence :',old_seq)
                        pass
            T = T * alpha 
            if debug:
                print("New Temperature=>",T)
            temp_cycle += 1
            if bestSolution > old_makeSpan:
               
                bestSolution = old_makeSpan
                bestSequence = old_seq
                if debug:
                    print("Best Solution Swap")
                    print('New Swap Sequence :', bestSequence)
                    print('New Sequence make span:', bestSolution)

        e = default_timer.__call__()
        if debug:
            print("Best Sequence",bestSequence)
            print("Best MakeSpan", bestSolution)
        #Result Sequence
        # seq=bestSequence
        # old_makeSpan=bestSolution
        print("Best Sequence",bestSequence)
        print("Best MakeSpan", bestSolution)
        seq = old_seq
        schedules = np.zeros((self.nb_machines, self.nb_jobs), dtype=dict)
        # schedule first job alone first
        task = {"name": "job_{}".format(
            seq[0] + 1), "start_time": 0, "end_time": self.data[0][seq[0]]}
        schedules[0][0] = task
        for m_id in range(1, self.nb_machines):
            start_t = schedules[m_id - 1][0]["end_time"]
            end_t = start_t + self.data[m_id][0]
            task = {"name": "job_{}".format(
                seq[0] + 1), "start_time": start_t, "end_time": end_t}
            schedules[m_id][0] = task

        for index, job_id in enumerate(seq[1::]):
            start_t = schedules[0][index]["end_time"]
            end_t = start_t + self.data[0][job_id]
            task = {"name": "job_{}".format(
                job_id + 1), "start_time": start_t, "end_time": end_t}
            schedules[0][index + 1] = task
            for m_id in range(1, self.nb_machines):
                start_t = max(schedules[m_id][index]["end_time"],
                              schedules[m_id - 1][index + 1]["end_time"])
                end_t = start_t + self.data[m_id][job_id]
                task = {"name": "job_{}".format(
                    job_id + 1), "start_time": start_t, "end_time": end_t}
                schedules[m_id][index + 1] = task
        t_t = e - s
        return seq, schedules, old_makeSpan, t_t





