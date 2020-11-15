from mesa.batchrunner import BatchRunner
from multiprocessing import Pool
from tqdm import tqdm
import copy
import pandas as pd
from itertools import product, count

class DrewBatchRunner(BatchRunner):

    def __init__(self, model_cls, nr_processes=1, **kwargs):
        super().__init__(model_cls, **kwargs)
        self.pool = Pool(nr_processes)

        def run_all(self):
            run_count = count()
            total_iterations, all_kwargs, all_param_values = self._make_model_arts()


            job_queue = []
            with tqdm(total_iterations, disable= not self.display_progress) as pbar:
                for i, kwargs in enumerate(all_kwargs):
                    param_values = all_param_values[i]
                    for _ in range(self.iterations):
                        job_queue.append(
                            self.pool.imap_unordered(
                                self.run_iteration,
                                (kwargs,),
                                (param_values),
                                (next(run_count),),
                            )
                        )
                    results = []
                    for task in job_queue:
                        for model_vars, agent_vars in list(task):
                            results.append((model_vars, agent_vars))
                            pbar.update()
                    
                    for model_vars, agent_vars in results:
                        if self.model_reports:
                            for model_key, model_val in model_vars.items():
                                self.model_vars[model_key] = model_val
                        if self.agent_reporters:
                            for agent_key, reports in agent_vars.items():
                                self.agent_vars[agent_key] = reports

