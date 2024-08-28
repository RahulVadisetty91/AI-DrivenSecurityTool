import os
import sys
import webbrowser
from platform import system
from traceback import print_exc
from typing import Callable, List, Tuple, Any
import logging

# Set up logging for better error tracking and debugging
logging.basicConfig(filename='hacking_tool.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants for repeated literals
CONTINUE_PROMPT = "\n\nPress ENTER to continue:"
INVALID_OPTION_MSG = "Please enter a valid option"
UNEXPECTED_ERROR_MSG = "Unexpected error occurred"
CONFIRM_UNINSTALL_MSG = "Are you sure you want to uninstall? (yes/no): "

def clear_screen():
    os.system("cls" if system() == "Windows" else "clear")

def validate_input(ip, val_range):
    val_range = val_range or []
    try:
        ip = int(ip)
        if ip in val_range:
            return ip
    except ValueError:
        logging.warning(f"Invalid input: {ip}")
        return None
    return None

class HackingTool(object):
    # About the HackingTool
    TITLE: str = ""
    DESCRIPTION: str = ""
    INSTALL_COMMANDS: List[str] = []
    INSTALLATION_DIR: str = ""
    UNINSTALL_COMMANDS: List[str] = []
    RUN_COMMANDS: List[str] = []
    OPTIONS: List[Tuple[str, Callable]] = []
    PROJECT_URL: str = ""

    def __init__(self, options=None, installable: bool = True, runnable: bool = True):
        options = options or []
        if isinstance(options, list):
            self.OPTIONS = []
            if installable:
                self.OPTIONS.append(('Install', self.install))
            if runnable:
                self.OPTIONS.append(('Run', self.run))
            self.OPTIONS.extend(options)
        else:
            raise TypeError("options must be a list of (option_name, option_fn) tuples")

    def show_info(self):
        desc = self.DESCRIPTION
        if self.PROJECT_URL:
            desc += '\n\t[*] ' + self.PROJECT_URL
        os.system(f'echo "{desc}"|boxes -d boy | lolcat')

    def show_options(self, parent=None):
        clear_screen()
        self.show_info()
        for index, option in enumerate(self.OPTIONS):
            print(f"[{index + 1}] {option[0]}")
        if self.PROJECT_URL:
            print(f"[{98}] Open project page")
        print(f"[{99}] Back to {parent.TITLE if parent is not None else 'Exit'}")
        option_index = input("Select an option : ").strip()
        try:
            option_index = int(option_index)
            if option_index - 1 in range(len(self.OPTIONS)):
                ret_code = self.OPTIONS[option_index - 1][1]()
                if ret_code != 99:
                    input(CONTINUE_PROMPT).strip()
            elif option_index == 98:
                self.show_project_page()
            elif option_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print(INVALID_OPTION_MSG)
            logging.error(f"Invalid option selected: {option_index}")
            input(CONTINUE_PROMPT).strip()
        except Exception as e:
            print_exc()
            logging.error(f"{UNEXPECTED_ERROR_MSG}: {e}")
            input(CONTINUE_PROMPT).strip()
        return self.show_options(parent=parent)

    def before_install(self):
        # Example AI-driven feature: Predictive check for system compatibility
        if not self._is_compatible_system():
            print("System is not compatible for installation.")
            return False
        return True

    def install(self):
        if self.before_install():
            if isinstance(self.INSTALL_COMMANDS, (list, tuple)):
                for INSTALL_COMMAND in self.INSTALL_COMMANDS:
                    os.system(INSTALL_COMMAND)
                self.after_install()

    def after_install(self):
        print("Successfully installed!")

    def before_uninstall(self) -> bool:
        """ Ask for confirmation from the user and return """
        return input(CONFIRM_UNINSTALL_MSG).strip().lower() == 'yes'

    def uninstall(self):
        if self.before_uninstall():
            if isinstance(self.UNINSTALL_COMMANDS, (list, tuple)):
                for UNINSTALL_COMMAND in self.UNINSTALL_COMMANDS:
                    os.system(UNINSTALL_COMMAND)
            self.after_uninstall()

    def after_uninstall(self):
        print("Successfully uninstalled!")

    def before_run(self):
        # Example AI-driven feature: Suggest possible commands based on previous runs
        self._suggest_commands()

    def run(self):
        self.before_run()
        if isinstance(self.RUN_COMMANDS, (list, tuple)):
            for RUN_COMMAND in self.RUN_COMMANDS:
                os.system(RUN_COMMAND)
            self.after_run()

    def after_run(self):
        print("Run completed!")

    def is_installed(self, dir_to_check=None):
        # Example AI-driven feature: Check installation status with an AI model
        print("Unimplemented: DO NOT USE")
        return "?"

    def show_project_page(self):
        webbrowser.open_new_tab(self.PROJECT_URL)

    def _is_compatible_system(self) -> bool:
        # Example system compatibility check (placeholder for real logic)
        return True

    def _suggest_commands(self):
        # Example AI-driven command suggestion (placeholder for real logic)
        print("Here are some suggested commands you might use:")

class HackingToolsCollection(object):
    TITLE: str = ""
    DESCRIPTION: str = ""
    TOOLS = []  # type: List[Any[HackingTool, HackingToolsCollection]]

    def __init__(self):
        pass

    def show_info(self):
        os.system("figlet -f standard -c {} | lolcat".format(self.TITLE))

    def show_options(self, parent=None):
        clear_screen()
        self.show_info()
        for index, tool in enumerate(self.TOOLS):
            print(f"[{index}] {tool.TITLE}")
        print(f"[{99}] Back to {parent.TITLE if parent is not None else 'Exit'}")
        tool_index = input("Choose a tool to proceed: ").strip()
        try:
            tool_index = int(tool_index)
            if tool_index in range(len(self.TOOLS)):
                ret_code = self.TOOLS[tool_index].show_options(parent=self)
                if ret_code != 99:
                    input(CONTINUE_PROMPT).strip()
            elif tool_index == 99:
                if parent is None:
                    sys.exit()
                return 99
        except (TypeError, ValueError):
            print(INVALID_OPTION_MSG)
            logging.error(f"Invalid tool index: {tool_index}")
            input(CONTINUE_PROMPT).strip()
        except Exception as e:
            print_exc()
            logging.error(f"{UNEXPECTED_ERROR_MSG}: {e}")
            input(CONTINUE_PROMPT).strip()
        return self.show_options(parent=parent)
