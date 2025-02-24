"""
Script initialises an Independant Logger for Semantic Search Module
"""
import logging


class ModuleLogger:
    """
    Class provides a Logger Object aimed for scripts utilising the Semantic Search Module \n
    The Logger will track the state of database requests and Responses and
    semantic search request and responses\n
    Logger Message Format:
         &#60;name&#62; at &#60;time&#62; (&#60;Level&#62;) :: &#60;Message&#62;
    """
    __logger: logging.Logger | None = None
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Method initialises (if required) and returns the Logger (object) 

        Returns
            Logger Object
        """
        if cls.__logger is None:
            #initialise Logger
            cls.__logger = logging.getLogger('semantic_search')
            cls.__logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(name)s at %(asctime)s (%(levelname)s) :: %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            cls.__logger.addHandler(handler)
        return cls.__logger
