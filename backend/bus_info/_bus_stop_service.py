from ._bus_stops_factory import BusStopsFactory as bus_factory
import os


class BusStopService:
    def __init__(self):
        self.factory = bus_factory()
        self.stop_list: list[bus_factory.BusStop] = self.factory.bus_stop_objects

    def return_stop_list_codes(self):
        codes = []
        for item in self.stop_list:
            code = item.code
            codes.append(code)
        return codes

    def refresh_stop_list(self):
        self.factory.update()

    def add_stop(self, filename):
        self.factory.add_new_stop(filename)
        self.stop_list = self.factory.bus_stop_objects

    def delete_stop(self, stop: bus_factory.BusStop):
        '''
        Deletes the BusStop object's corresponding .json file and the object
        from the self.stop_list[].
        Returns the deleted stop if operation succeeded and None if not.
        '''
        json_file = f'{stop.json_file_name}.json'
        path = os.path.join("backend", "stops-JSON", json_file)
        try:
            self.stop_list.remove(stop)
            os.remove(path)
            return stop
        except Exception as e:
            print(e)
            return None
