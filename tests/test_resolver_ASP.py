import importlib
import importlib.util
spec = importlib.util.spec_from_file_location('src', 'src/py/resolver_ASP.py')
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)

resolver_ASP = getattr(modulo, 'resolver_ASP')