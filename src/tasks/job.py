# INSTRUCTION:
# def job_exectue():
#     print("This function will be executed like a worker job")
###############################################################
from typing import Any

from loguru import logger

from .base import task_service
from .utils import get_json_response, import_string


#############################################################################
# INFO: Apply async servicce module - in app/services/<your_service>
# If your service have func like
# class YourService():
#       def your_func(*arg,**kwargs):
#           pass
# your_service = YourService()
#
#
# apply_async(your_service.your_func,*arg,**kwargs)
#
#############################################################################
@task_service.task()  # type:ignore
@get_json_response
def run_service(obj_name: str, method_name: str, *args: tuple, **kwargs: dict) -> Any:
    obj = import_string(obj_name)
    fn = getattr(obj, method_name)
    logger.info(f"Run Task: {obj_name}.{method_name}")

    return fn(*args, **kwargs)


def apply_async(fn: Any, *args: Any, **kwargs: Any) -> Any:
    module_name = fn.__module__
    method_name = fn.__name__
    err = Exception(f"Can not support module name: {module_name}")
    roots = module_name.split(".")
    if len(roots) != 4:
        raise err
    if roots[0] == "src" and roots[1] == "app":
        obj_name = f"{module_name}.{roots[-1]}_service"
    else:
        raise err
    if not args == ():
        fn_args = [obj_name, method_name].append(args)
    fn_args = [obj_name, method_name]
    fn_kwargs = kwargs
    return run_service.apply_async(args=fn_args, kwargs=fn_kwargs)
