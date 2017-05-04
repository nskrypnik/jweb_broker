
class BaseTasksLookout:

    def find(self, job_data):
        '''This function should find corresponding task based on data provided
           in job_data parameter. Should be implemented in subclass
        '''
        raise NotImplemented('Find function should be implemented in subclass')
