import threading
import logging
from openfb.core import fb_interface
import os
from openfb.data_model_fboot import utils
import queue

class FB(threading.Thread, fb_interface.FBInterface):

    def __init__(self, fb_name, fb_type, fb_obj, fb_xml, monitor=None, opc_mapping=None):
        threading.Thread.__init__(self, name=fb_name)
        fb_interface.FBInterface.__init__(self, fb_name, fb_type, fb_xml, monitor)

        self.fb_obj = fb_obj
        self.opc_mapping = opc_mapping
        self.kill_event = threading.Event()
        self.execution_end = threading.Event()
        self.ua_variables_update = None
        self.update_variables_fboot = None
        self.fb_type = fb_type

        if hasattr(fb_obj, 'set_on_event_callback'):
            fb_obj.set_on_event_callback(self._trigger_event)

        if fb_type != 'TEST_FB' and fb_name != 'START':
            # Gets the dir path to the py and fbt files
            root_path = utils.get_fb_files_path(fb_type)
            # Gets the file path to the python file
            py_path = os.path.join(root_path, fb_type + '.py')
            message_queue = queue.Queue()
            self.message_queue = message_queue

    def run(self):
        logging.info('fb {0} started.'.format(self.fb_name))

        while not self.kill_event.is_set():

            if self.fb_type != 'TEST_FB':
                try:
                    self.fb_obj = self.message_queue.get(False)
                    logging.info('Updated {0}'.format(self.fb_type))
                except queue.Empty:
                    pass

            # clears the event when starts the execution
            self.execution_end.clear()

            self.wait_event()

            if self.kill_event.is_set():
                break

            inputs = self.read_inputs()


            try:
                outputs = self.fb_obj.schedule(*inputs)
                logging.debug(f"Inputs: {inputs}, Module ouputs:{outputs}")

            except TypeError as error:
                logging.error('invalid number of arguments (check if fb method args are in fb_type.fbt)')
                logging.exception(error)
                logging.error(error)
                # Stops the thread
                break

            except Exception as ex:
                logging.error(ex)
                logging.exception(ex)
                # Stops the thread
                break

            else:
                # If the thread blocks inside any fb method
                if self.kill_event.is_set():
                    break

                if outputs is None:
                    logging.error('Outputs are null, please check {0}.py'.format(self.fb_name))
                    # Stops the thread
                    break

                self.update_outputs(outputs)

                # updates the opc-ua interface
                if self.ua_variables_update is not None:
                    self.ua_variables_update()
                
                if self.update_variables_fboot is not None:
                    self.update_variables_fboot()


                # sends a signal when ends execution
                self.execution_end.set()

    def _trigger_event(self, *args):
        """
        Callback for async event generators (OF_E_CYCLE, OF_E_TRAIN, OF_E_N_TABLE, etc.)
        Triggers output event from background thread.
        
        Different FB types call with different argument patterns:
        - OF_E_CYCLE: callback('EO', event_value)
        - OF_E_TRAIN, OF_E_TABLE: callback(event_value, output_var) 
        - OF_E_N_TABLE: callback('EO0', event_value, index)
        - OF_E_BLINK: callback('CNF', event_value, output_var)
        """
        if len(args) == 0:
            logging.warning("_trigger_event called with no arguments")
            return
        
        # Determine if first argument is an event name (string) or event value
        first_arg = args[0]
        
        if isinstance(first_arg, str):
            # Pattern: callback(event_name, event_value, ...)
            event_name = first_arg
            event_value = args[1] if len(args) > 1 else 1
        else:
            # Pattern: callback(event_value, ...)
            # Default event name is 'EO' for OF_E_CYCLE, OF_E_TRAIN, OF_E_TABLE
            event_name = 'EO'
            event_value = first_arg
        
        # Send event to all connected FBs
        if event_name in self.output_connections:
            for connection in self.output_connections[event_name]:
                connection.send_event(event_value)

    def stop(self):

        self.stop_thread = True

        self.kill_event.set()
        self.push_event('unblock', 1)

        try:
            self.fb_obj.__del__()
        except AttributeError as exc:
            logging.warning('can not delete the fb object.')
            logging.warning(exc)

        logging.info('fb {0} stopped.'.format(self.fb_name))
