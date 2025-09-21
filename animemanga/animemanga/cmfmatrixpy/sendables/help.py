import inspect

class SendableHelp:
    """Stylized help message for commands"""

    def to_help(help: str=None, command_name: str=None, func=None, func_text=[]):
        usage = ""
        if help:
            usage += help + "\n"
        if command_name:
            usage += "> **Usage:** !" + command_name + " "
        if func:
            for parameter in self.get_parameters(func):
                usage += "<" + parameter + "> "
        elif func_text:
            for parameter in func_text:
                usage += "<" + parameter + "> "
        return usage

    def get_parameters(func):
        sig = inspect.signature(func)
        return [str(s) for k,s in sig.parameters.items()]
